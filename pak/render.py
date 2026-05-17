"""Unified renderer for the upstream Pak128.Britain blends.

One pipeline parameterised by a `Viewpoint` describes both the
square-dimetric upstream view (used as the calibration baseline
against the published pak PNGs) and the hex projection this project
ships.  The same scene-prep, mesh-bake, per-facing-render path
serves both -- viewpoints differ only in camera placement, sun
direction, the per-facing list, and an extrinsic 4x4 baked into
the mesh (identity for square, hex shear for hex).

The .blend is treated as pure model data: any existing Camera,
Sphere or Lamp objects are deleted at load and replaced by ones
the Viewpoint describes.  This makes the bake reproducible
regardless of how the blend was saved.

Mesh strategy: bake `matrix_world` into mesh vertex data once,
then per facing apply `extrinsic @ rot_z(model_rot) @ fit` via
`mesh.transform()`.  See CLAUDE.md -> "silent-failure landmines"
for why we don't carry the projection on a parent Empty
(matrix_basis decomposition drops shear) and why we exit edit mode
up front (the BMesh edit buffer bypasses v.co writes).

Run as:

    blender -b <blend_path> -P pak/render.py -- \\
        --out <dir> --name <stem> --viewpoint hex|square \\
        [--keep-per-facing] [--cols-per-row N]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from math import radians
from pathlib import Path
from typing import Optional


HERE = Path(__file__).resolve().parent
# Put the repo root on sys.path so `pak.<module>` imports resolve.
# `hex_synth` uses `from .way import …`, so we need the package form,
# not a flat sys.path on the `pak/` dir.  Mirrors `pak/bake_way.py`.
sys.path.insert(0, str(HERE.parent))


@dataclass
class Facing:
    """One sprite direction within a Viewpoint.

    `model_translation` shifts the rotated mesh in world XY before the
    extrinsic shear — used by multi-tile building bakes to bring one
    footprint cell to world origin per facing so the standard hex
    camera renders that single cell's content."""
    label: str
    camera_location: tuple[float, float, float]
    camera_rotation_euler: tuple[float, float, float]  # radians
    sun_rotation_euler: tuple[float, float, float]  # radians
    model_rot_z_deg: float = 0.0  # rotation applied to the mesh after fit
    model_translation: tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class Viewpoint:
    """Self-contained recipe for rendering one asset N ways.

    `ortho_scale=None` means "use the blend's authored ortho_scale" —
    used by `square_building` to match upstream's rendering exactly
    (which honours each blend's own camera, e.g. 12 for buildings vs
    24 for vehicles).  A float pins the camera to that value
    regardless of what the blend declared (used by SQUARE_VIEWPOINT at
    24 and HEX_VIEWPOINT at 2R, both of which want a fixed pak-side
    scale)."""
    name: str
    image_width: int
    ortho_scale: Optional[float]
    # `None` means "use the blend's authored sun energy, scaled by the
    # engine-substitution factor declared in `sun_energy_scale`".  A
    # float pins the value directly -- used by SQUARE_VIEWPOINT and
    # HEX_VIEWPOINT to assert the upstream 0.028 verbatim under Cycles
    # (the empirical vehicle/way substitute for the lost BI authoring
    # engine; not literally what upstream rendered with).
    sun_energy: Optional[float]
    # "hex": centre + z_floor + INTRA_TILE_PER_BLEND_UNIT scale.
    # "none": identity (used by SQUARE_VIEWPOINT — operates in blend
    # coords so it can pixel-diff against upstream's published cells).
    fit_kind: str
    extrinsic: Optional[tuple]  # 4x4 row-major tuple, or None for identity
    facings: list[Facing]
    # Engine-substitution multiplier applied to the authored sun energy
    # when `sun_energy is None`.  BI-authored 0.028 reads as near-zero
    # under EEVEE's PBR pipeline; the building viewpoints scale by
    # ≈71.4 (= 2.0/0.028) to approximate BI's apparent brightness.
    sun_energy_scale: float = 1.0
    # Vehicles & ways: "CYCLES".  Buildings: "BLENDER_EEVEE" (BI's
    # use_nodes=False materials render closer to upstream under EEVEE
    # than Cycles).  Both are empirical substitutes for upstream's
    # actual authoring engine (Blender Internal under 2.79, dropped
    # in 2.80) -- see CLAUDE.md -> "Building-bake architecture".
    # "BLENDER_WORKBENCH" available for flat-shading paths (ways).
    engine: str = "CYCLES"


# Per-material texture-tile frequency on Generated coords.  Default 8.0
# (8 cycles per object-bbox axis) reads as small bricks on a typical
# wall.  Pavement is a single ground plane that wants finer aggregate
# detail (more cycles); roof tiles read smaller than wall bricks.
_TEX_TILE: dict[str, float] = {
    "brick": 8.0,
    "roof": 12.0,
    "roofside": 12.0,
    "pavement": 6.0,
}


def _reload_external_textures(bpy) -> None:
    """Britain blends reference textures via relative filepaths like
    `//../../../textures/flemish-bond-improved.png` that don't resolve
    from the blend's location in `.cache/blends/<sha>/`.  For every
    image data block whose file failed to load (size 0), look up its
    basename in the blends repo's `textures/` directory via fetch_blend
    and rewrite the filepath.  No-op for images that loaded fine."""
    from pak.fetch_blend import fetch as fetch_blend
    for img in bpy.data.images:
        if img.size[0] != 0:
            continue
        if img.type != "IMAGE":
            continue  # skip RENDER_RESULT / COMPOSITING / UV_TEST built-ins
        base = img.filepath.rsplit("/", 1)[-1] if img.filepath else img.name
        if not base:
            continue
        try:
            local = fetch_blend(f"textures/{base}")
        except SystemExit:
            continue
        img.filepath = str(local)
        try:
            img.reload()
        except RuntimeError:
            pass


def _bsdf_node(nt):
    """A flat-shading Principled BSDF (roughness=1, specular=0) — the
    EEVEE substitute for BI's default Lambert."""
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 1.0
    try:
        bsdf.inputs["Specular IOR Level"].default_value = 0.0
    except KeyError:
        bsdf.inputs["Specular"].default_value = 0.0
    return bsdf


def _bind_textures_via_nodes(bpy) -> None:
    """Reconstruct BI material->texture bindings via the name-match
    heuristic against `bpy.data.textures` (which survives the
    2.80 stripping of `material.texture_slots`).  Builds a Principled
    BSDF node graph per matched material: Generated coords -> Mapping
    (scale `tile_n`) -> ImageTexture -> Multiply by fallback diffuse
    -> Base Color.  Materials with no image-texture match but a name
    in `procedural_noise_mats` (Hedge) get a Noise->ColorRamp node
    graph instead -- substitutes BI's lost CLOUDS texture.

    See CLAUDE.md -> "Building-bake architecture" for what this
    approximation does and does not recover from upstream's BI render.

    A richer recovery path -- reading BI's authoritative MTex slot
    data from the .blend binary (`pak/blend_slots.py`) -- is staged
    but not wired in; see TODO."""

    tex_by_name: dict[str, "bpy.types.Texture"] = {}
    for t in bpy.data.textures:
        if t.type == "IMAGE" and t.image and t.image.size[0] > 0:
            tex_by_name[t.name.lower()] = t

    # Fallback hand-encoded overrides for material/texture name pairs
    # the prefix matcher misses.  Only kicks in when slot-data extraction
    # didn't bind this material.
    explicit_map = {
        "pavement": "pavings",
        "roof": "brick",
        "roofside": "brick",
    }

    def match_texture(mat_name: str):
        key = mat_name.lower()
        if key in explicit_map and explicit_map[key] in tex_by_name:
            return tex_by_name[explicit_map[key]]
        for tname, tex in tex_by_name.items():
            if key == tname or key.startswith(tname) or tname.startswith(key):
                return tex
        return None

    procedural_noise_mats = {"hedge"}

    def build_image_material(m, tex):
        fallback_diffuse = tuple(m.diffuse_color)
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        bsdf = _bsdf_node(nt)
        tex_img = nt.nodes.new("ShaderNodeTexImage")
        tex_img.image = tex.image
        coord = nt.nodes.new("ShaderNodeTexCoord")
        mapping = nt.nodes.new("ShaderNodeMapping")
        mapping.vector_type = "POINT"
        tile_n = _TEX_TILE.get(m.name.lower(), 8.0)
        mapping.inputs["Scale"].default_value = (tile_n, tile_n, tile_n)
        mul = nt.nodes.new("ShaderNodeMixRGB")
        mul.blend_type = "MULTIPLY"
        mul.inputs["Fac"].default_value = 1.0
        mul.inputs["Color2"].default_value = (*fallback_diffuse[:3], 1.0)
        nt.links.new(coord.outputs["Generated"], mapping.inputs["Vector"])
        nt.links.new(mapping.outputs["Vector"], tex_img.inputs["Vector"])
        nt.links.new(tex_img.outputs["Color"], mul.inputs["Color1"])
        nt.links.new(mul.outputs["Color"], bsdf.inputs["Base Color"])
        nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
        m.diffuse_color = fallback_diffuse

    def build_noise_material(m):
        fallback_diffuse = tuple(m.diffuse_color)
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        bsdf = _bsdf_node(nt)
        noise = nt.nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = 50.0
        noise.inputs["Detail"].default_value = 2.0
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = 0.4
        ramp.color_ramp.elements[0].color = (
            fallback_diffuse[0] * 0.6,
            fallback_diffuse[1] * 0.6,
            fallback_diffuse[2] * 0.6,
            1.0,
        )
        ramp.color_ramp.elements[1].position = 0.6
        ramp.color_ramp.elements[1].color = (
            min(1.0, fallback_diffuse[0] * 1.2),
            min(1.0, fallback_diffuse[1] * 1.2),
            min(1.0, fallback_diffuse[2] * 1.2),
            1.0,
        )
        coord = nt.nodes.new("ShaderNodeTexCoord")
        nt.links.new(coord.outputs["Generated"], noise.inputs["Vector"])
        nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
        nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
        m.diffuse_color = fallback_diffuse

    for m in bpy.data.materials:
        if m.use_nodes:
            continue
        key = m.name.lower()
        if key in procedural_noise_mats:
            build_noise_material(m)
            continue
        tex = match_texture(m.name)
        if tex is None:
            continue
        build_image_material(m, tex)


@dataclass
class BlendAuthored:
    """Parameters captured from the .blend before its scene objects are
    stripped.  The .blend is treated as pure model data — every
    render-time prop is reinstalled from the Viewpoint — but the artist's
    authored choices land here and feed back in.

    `ortho_scale` drives the per-asset `INTRA_TILE_PER_BLEND_UNIT =
    2*HEX_TILE_RADIUS / ortho_scale` (vehicles=24, many buildings=12).
    `sun_energy` carries the upstream-authored 0.028 that BI rendered
    against; modern engines apply `viewpoints._BI_TO_EEVEE_SUN_SCALE`
    to compensate.  Sun color isn't extracted — all Britain blends
    ship `(1,1,1)` (white), the default a freshly-installed SUN lamp
    gets anyway.  World ambient also isn't extracted: authored
    `world.color` was the BI background sky, not the ambient term,
    and modern EEVEE's `world.color` IS the ambient term — so the
    authored value would be the wrong thing to plug in."""
    ortho_scale: Optional[float] = None
    sun_energy: Optional[float] = None


def _strip_scene(bpy) -> BlendAuthored:
    """Capture authored Camera/Sun parameters into a BlendAuthored, then
    remove the corresponding scene objects so the Viewpoint can install
    its own.  `Sphere` is the upstream sun-visualisation parent mesh
    (Lamp.001 is parented to it); both go."""
    authored = BlendAuthored()
    for obj in list(bpy.context.scene.objects):
        if obj.type == "CAMERA":
            if authored.ortho_scale is None and obj.data.type == "ORTHO":
                authored.ortho_scale = float(obj.data.ortho_scale)
            bpy.data.objects.remove(obj, do_unlink=True)
        elif obj.type == "LIGHT":
            la = obj.data
            if authored.sun_energy is None and la.type == "SUN":
                authored.sun_energy = float(la.energy)
            bpy.data.objects.remove(obj, do_unlink=True)
        elif obj.name == "Sphere":
            bpy.data.objects.remove(obj, do_unlink=True)
    return authored


def _install_camera_and_sun(bpy, viewpoint: Viewpoint,
                            authored: BlendAuthored):
    """Create one camera and one SUN light, configured per the Viewpoint
    with fallback to authored values for fields the Viewpoint defers
    (sun_energy=None, ortho_scale=None).  Per-facing pose changes
    (location, rotation) happen in the render loop."""
    ortho = (viewpoint.ortho_scale
             if viewpoint.ortho_scale is not None
             else authored.ortho_scale)
    if ortho is None:
        raise SystemExit(
            "Viewpoint declared ortho_scale=None and blend has no ortho camera"
        )
    cam_data = bpy.data.cameras.new("_render_camera")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = ortho
    cam = bpy.data.objects.new("_render_camera", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.rotation_mode = "XYZ"

    if viewpoint.sun_energy is not None:
        sun_energy = viewpoint.sun_energy
    elif authored.sun_energy is not None:
        sun_energy = authored.sun_energy * viewpoint.sun_energy_scale
    else:
        raise SystemExit(
            "Viewpoint declared sun_energy=None and blend has no SUN light"
        )
    sun_data = bpy.data.lights.new("_render_sun", type="SUN")
    sun_data.energy = sun_energy
    sun = bpy.data.objects.new("_render_sun", sun_data)
    bpy.context.scene.collection.objects.link(sun)
    sun.rotation_mode = "XYZ"

    scn = bpy.context.scene
    scn.render.resolution_x = viewpoint.image_width
    scn.render.resolution_y = viewpoint.image_width
    scn.render.resolution_percentage = 100
    scn.render.film_transparent = True
    scn.render.image_settings.color_mode = "RGBA"
    # Match upstream's saved colour-management: Raw view transform,
    # sRGB display, gamma 1.0, no exposure.  Britain blends ship these
    # values; some get clobbered if the blend was re-saved under a
    # newer Blender with Filmic defaulting on.
    scn.view_settings.view_transform = "Raw"
    scn.view_settings.look = "None"
    scn.view_settings.exposure = 0.0
    scn.view_settings.gamma = 1.0
    scn.display_settings.display_device = "sRGB"
    # Pin Cycles knobs that are otherwise non-deterministic across CI
    # runs even on identical hardware: threads (multi-threaded reduction
    # order), adaptive sampling (per-pixel termination on a noise
    # estimate), the denoiser (the blend may save it on), and the
    # sample seed (the blend may save a non-zero value).
    scn.render.threads_mode = "FIXED"
    scn.render.threads = 1
    scn.cycles.use_denoising = False
    scn.cycles.use_adaptive_sampling = False
    scn.cycles.seed = 0

    scn.render.engine = viewpoint.engine
    if viewpoint.engine == "BLENDER_WORKBENCH":
        scn.display.shading.light = "FLAT"
        scn.display.shading.color_type = "MATERIAL"
        scn.display.shading.show_specular_highlight = False
    elif viewpoint.engine == "BLENDER_EEVEE":
        # taa_render_samples=8 gives proper edge alpha-AA (1 writes
        # 0-or-255 only and drops the edge ring).  GTAO/bloom/SSR off
        # for determinism across CI runners.
        scn.eevee.taa_render_samples = 8
        scn.eevee.use_gtao = False
        scn.eevee.use_bloom = False
        scn.eevee.use_ssr = False
        scn.eevee.use_volumetric_lights = False
        scn.eevee.use_soft_shadows = False
        scn.eevee.use_shadow_high_bitdepth = True
        # Diffuse fill calibrated against `res_1600_kg_01` upstream.
        if scn.world is not None:
            scn.world.use_nodes = False
            try:
                scn.world.color = (0.30, 0.30, 0.30)
            except AttributeError:
                pass

    return cam, sun


def _exit_edit_mode(bpy) -> None:
    """Upstream blends occasionally ship with one mesh stuck in edit
    mode (e.g. 4wheel-1850's body Cube.009).  Blender renders the BMesh
    edit buffer rather than `obj.data` until the object leaves edit
    mode -- our mesh.transform() / v.co writes are invisible to the
    renderer otherwise.  See CLAUDE.md -> "Edit-mode meshes"."""
    prev_active = bpy.context.view_layer.objects.active
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH" and obj.data.is_editmode:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = prev_active


def _collection_renders(bpy, coll, cache):
    """Walk the collection ancestry: a collection contributes to the
    render only if neither it nor any ancestor sets hide_render.

    Britain blends keep livery variants, alt-detail meshes and
    render-time-only scaffolding (flagpoles, ensigns) in collections
    flagged hide_render; vertex iteration must respect that or fit
    math gets dragged by geometry that never renders."""
    if coll.name in cache:
        return cache[coll.name]
    if coll.hide_render:
        cache[coll.name] = False
        return False
    for parent in bpy.data.collections:
        if coll.name in parent.children.keys():
            if not _collection_renders(bpy, parent, cache):
                cache[coll.name] = False
                return False
    cache[coll.name] = True
    return True


def _bake_world_into_meshes(bpy, mathutils):
    """Bake each renderable mesh's matrix_world into its vertex data
    and clear the object's transform to identity; return a list of
    (obj, original_world_coords) records.  The records' `orig` is the
    canonical world position of each vertex, used to reset the mesh
    between facings (via `_apply_facing`).

    Linked-mesh data is unshared up front so per-instance baked
    transforms don't collide."""
    M = mathutils.Matrix
    scn = bpy.context.scene

    _exit_edit_mode(bpy)

    cache: dict = {}
    def renders(obj):
        return (not obj.hide_render
                and all(_collection_renders(bpy, c, cache) for c in obj.users_collection))

    rendered = [o for o in scn.objects if o.type == "MESH" and renders(o)]

    # Snapshot every matrix_world before any mutation: mutating a
    # parent's transform mid-loop silently shifts its children's
    # effective world position.
    snapshots = [(o, o.matrix_world.copy()) for o in rendered]

    seen_data = set()
    records = []
    for obj, mw in snapshots:
        if obj.data.users > 1 or id(obj.data) in seen_data:
            obj.data = obj.data.copy()
        seen_data.add(id(obj.data))
        obj.data.transform(mw)
        if obj.parent is not None:
            obj.parent = None
            obj.matrix_parent_inverse = M.Identity(4)
        obj.matrix_basis = M.Identity(4)
        orig = [v.co.copy() for v in obj.data.vertices]
        records.append((obj, orig))

    # Force the matrix_world cache to refresh: assignments to
    # matrix_basis are lazy, and the renderer otherwise reads stale
    # non-identity matrices for objects with non-unit scale,
    # double-applying their original transform on top of the baked mesh.
    bpy.context.view_layer.update()
    return records


def _compute_fit(mathutils, records, fit_kind: str,
                 blend_ortho: Optional[float] = None):
    """Build the world->fitted-frame 4x4 the per-facing transform composes
    over.  `fit_kind="none"` is identity (model renders at its native
    blend-coord scale).  `fit_kind="hex"` centres the XY bounding box
    on origin, drops the lowest visible vertex to z=0, and scales by
    `2 * HEX_TILE_RADIUS / blend_ortho` to convert from blend coords into
    the pakset's intra-tile coord system.  `blend_ortho` is the blend's
    authored ortho_scale read by `_strip_scene` — falls back to the
    pakset-default `UPSTREAM_ORTHO_SCALE` (24, vehicle-blend convention)
    when the blend has no camera.  Buildings tend to ship at
    ortho_scale=12 (twice the per-cell zoom) and honouring that per-
    asset is what makes them render at upstream's per-pixel scale
    instead of half-size."""
    M = mathutils.Matrix
    if fit_kind == "none":
        return M.Identity(4)
    if fit_kind == "hex":
        from pak.hex_synth import HEX_TILE_RADIUS, UPSTREAM_ORTHO_SCALE  # noqa: E402
        ortho = blend_ortho if blend_ortho is not None else UPSTREAM_ORTHO_SCALE
        scale = 2.0 * HEX_TILE_RADIUS / ortho
        xs = []; ys = []; zs = []
        for _, orig in records:
            for c in orig:
                xs.append(c.x); ys.append(c.y); zs.append(c.z)
        if not xs:
            raise SystemExit("no renderable mesh vertices to fit")
        cx = (min(xs) + max(xs)) / 2.0
        cy = (min(ys) + max(ys)) / 2.0
        z_floor = min(zs)
        S = M.Diagonal((scale, scale, scale, 1.0))
        return S @ M.Translation((-cx, -cy, -z_floor))
    raise SystemExit(f"unknown fit_kind: {fit_kind!r}")


def _apply_facing(records, M_target) -> None:
    """Rewrite each mesh's vertices to `M_target @ canonical_world_co`.
    Called once per facing; matrix_world stays the identity."""
    for obj, orig in records:
        for v, oc in zip(obj.data.vertices, orig):
            v.co = M_target @ oc
        obj.data.update()


def _load_rgba(bpy, path: Path):
    """Read a PNG via Blender into a top-down (h, w, 4) numpy float32
    array.  Blender stores image pixels bottom-up; flip on load so the
    in-memory convention matches PIL (and bbox printouts read
    row-from-top)."""
    import numpy as np
    img = bpy.data.images.load(str(path))
    try:
        w, h = img.size[0], img.size[1]
        buf = np.empty(w * h * 4, dtype=np.float32)
        img.pixels.foreach_get(buf)
    finally:
        bpy.data.images.remove(img)
    return buf.reshape(h, w, 4)[::-1].copy()


def _save_atlas(bpy, atlas, name: str, path: Path) -> None:
    """Write a top-down (h, w, 4) numpy array as a PNG via bpy."""
    h, w = atlas.shape[:2]
    img = bpy.data.images.new(name=name, width=w, height=h, alpha=True)
    try:
        flipped = atlas[::-1].astype("float32", copy=False)
        img.pixels.foreach_set(flipped.ravel())
        img.filepath_raw = str(path)
        img.file_format = "PNG"
        img.save()
    finally:
        bpy.data.images.remove(img)


def _print_atlas_summary(out_path: Path, cells, cols: int, rows: int) -> None:
    """Echo per-cell bbox to stdout (debug aid mirroring
    `hextrans-pak128/tools/threed/bespoke.py::bake_atlas`'s output)."""
    import numpy as np
    h, w = cells[0][1].shape[:2]
    label_w = max(len(label) for label, _ in cells)
    print(f"wrote {out_path} ({cols * w}x{rows * h} px, {len(cells)} cells)")
    for i, (label, cell) in enumerate(cells):
        r, c = divmod(i, cols)
        mask = cell[..., 3] > 0
        if mask.any():
            ys, xs = np.where(mask)
            bbox = (f"bbox=({int(xs.min())},{int(ys.min())})-"
                    f"({int(xs.max())},{int(ys.max())}) px={int(mask.sum())}")
        else:
            bbox = "EMPTY"
        print(f"  r{r}c{c}: {label:<{label_w}s} {bbox}")


def render_atlas(bpy, mathutils, viewpoint: Viewpoint, out_dir: Path,
                 name: str, cols_per_row: Optional[int] = None,
                 keep_per_facing: bool = False) -> None:
    """Render `viewpoint.facings` of the currently loaded blend.  Writes
    `<out_dir>/<name>.png` (atlas).  With `keep_per_facing=True`, also
    writes `<out_dir>/<name>_<label>.png` per facing -- used by the
    calibration diff against the upstream pak."""
    import numpy as np

    authored = _strip_scene(bpy)
    if viewpoint.engine == "BLENDER_EEVEE":
        _reload_external_textures(bpy)
        _bind_textures_via_nodes(bpy)
    cam, sun = _install_camera_and_sun(bpy, viewpoint, authored)
    records = _bake_world_into_meshes(bpy, mathutils)
    fit = _compute_fit(mathutils, records, viewpoint.fit_kind,
                       authored.ortho_scale)
    extrinsic = (mathutils.Matrix(viewpoint.extrinsic) if viewpoint.extrinsic
                 else mathutils.Matrix.Identity(4))

    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = out_dir / ".render_tmp"
    tmp_dir.mkdir(exist_ok=True)

    scn = bpy.context.scene
    cells = []
    try:
        for facing in viewpoint.facings:
            cam.location = facing.camera_location
            cam.rotation_euler = facing.camera_rotation_euler
            sun.rotation_euler = facing.sun_rotation_euler
            M_target = (extrinsic
                        @ mathutils.Matrix.Translation(facing.model_translation)
                        @ mathutils.Matrix.Rotation(radians(facing.model_rot_z_deg), 4, "Z")
                        @ fit)
            _apply_facing(records, M_target)
            tmp_path = tmp_dir / f"{facing.label}.png"
            scn.render.filepath = str(tmp_path)
            bpy.ops.render.render(animation=False, write_still=True)
            cells.append((facing.label, _load_rgba(bpy, tmp_path)))
            if keep_per_facing:
                shutil.copy(tmp_path, out_dir / f"{name}_{facing.label}.png")

        cols = cols_per_row or len(cells)
        rows = (len(cells) + cols - 1) // cols
        h, w = cells[0][1].shape[:2]
        atlas = np.zeros((rows * h, cols * w, 4), dtype=np.float32)
        for i, (_, cell) in enumerate(cells):
            r, c = divmod(i, cols)
            atlas[r * h:(r + 1) * h, c * w:(c + 1) * w] = cell
        out_path = out_dir / f"{name}.png"
        _save_atlas(bpy, atlas, name, out_path)
        _print_atlas_summary(out_path, cells, cols, rows)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--viewpoint", required=True,
                    choices=["hex", "square", "hex_building", "square_building"])
    ap.add_argument("--keep-per-facing", action="store_true",
                    help="write per-facing PNGs alongside the atlas (used by diff)")
    ap.add_argument("--cols-per-row", type=int, default=None)
    ap.add_argument("--building-footprint", default=None,
                    help="X,Y,L,H — footprint (dims_x, dims_y, layouts, "
                         "heights) for viewpoint=hex_building or "
                         "square_building; required for those modes")
    return ap.parse_args(argv)


def main(argv):
    import bpy
    import mathutils
    from pak.viewpoints import (
        HEX_VIEWPOINT, SQUARE_VIEWPOINT,
        building_hex_viewpoint, building_square_viewpoint,
    )

    args = _parse_args(argv)
    if args.viewpoint == "hex":
        vp = HEX_VIEWPOINT
    elif args.viewpoint == "square":
        vp = SQUARE_VIEWPOINT
    elif args.viewpoint in ("hex_building", "square_building"):
        if not args.building_footprint:
            raise SystemExit(
                f"--viewpoint {args.viewpoint} requires --building-footprint X,Y,L,H"
            )
        parts = [int(s) for s in args.building_footprint.split(",")]
        if len(parts) == 3:
            parts.append(1)  # heights=1 default for back-compat
        dx, dy, l, h = parts
        factory = (building_hex_viewpoint if args.viewpoint == "hex_building"
                   else building_square_viewpoint)
        vp = factory(layouts=l, dims_x=dx, dims_y=dy, heights=h)
    else:
        raise SystemExit(f"unknown viewpoint: {args.viewpoint!r}")
    render_atlas(bpy, mathutils, vp, args.out, args.name,
                 cols_per_row=args.cols_per_row,
                 keep_per_facing=args.keep_per_facing)
    return 0


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(argv))
