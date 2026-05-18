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
    camera renders that single cell's content.  `model_scale` scales
    the mesh uniformly after fit — used by tree bakes to render the
    same model at successive growth stages."""
    label: str
    camera_location: tuple[float, float, float]
    camera_rotation_euler: tuple[float, float, float]  # radians
    sun_rotation_euler: tuple[float, float, float]  # radians
    model_rot_z_deg: float = 0.0  # rotation applied to the mesh after fit
    model_translation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    model_scale: float = 1.0


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
    ortho_scale: float | None
    # `None` means "use the blend's authored sun energy, scaled by the
    # engine-substitution factor declared in `sun_energy_scale`".  A
    # float pins the value directly -- used by SQUARE_VIEWPOINT and
    # HEX_VIEWPOINT to assert the upstream 0.028 verbatim under Cycles
    # (the empirical vehicle/way substitute for the lost BI authoring
    # engine; not literally what upstream rendered with).
    sun_energy: float | None
    # "hex": centre + z_floor + INTRA_TILE_PER_BLEND_UNIT scale.
    # "none": identity (used by SQUARE_VIEWPOINT — operates in blend
    # coords so it can pixel-diff against upstream's published cells).
    fit_kind: str
    extrinsic: tuple | None  # 4x4 row-major tuple, or None for identity
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
    # Object names stripped from the scene on entry (in addition to all
    # Camera and Light objects, which always go).  Default `("Sphere",)`
    # drops upstream's sun-direction visualizer mesh.  Tree blends add
    # `"Plane"` -- a large grey ground reference that upstream's
    # rendered PNGs don't show (presumably hidden via a separate
    # render-time script that doesn't ship with the blend).
    strip_meshes: tuple[str, ...] = ("Sphere",)


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


def _resolve_image(bpy, image_name: str):
    """Look up `bpy.data.images[image_name]`; return None if missing
    or if the file failed to load (size 0).  The seeder writes the
    BI slot's Image ID name verbatim, so this is a direct dict-style
    lookup -- no fuzzy matching."""
    img = bpy.data.images.get(image_name)
    if img is None or img.type != "IMAGE" or img.size[0] == 0:
        return None
    return img


def _build_image_material(bpy, m, tex_img, mat_spec) -> None:
    """Wire `m` as `<coord> -> Mapping(scale=size) -> Image ->
    Mul(diffuse) -> Principled BSDF`.

    Coord source by `mat_spec.texco`:
    - "GLOB": Attribute("blend_world_pos") populated by
      `_bake_world_into_meshes`.  Reads the original blend-frame world
      position, untouched by `_apply_facing`'s per-facing v.co rewrites,
      so the texture stays projected from a fixed world frame the way
      BI did when only the camera moved across facings.  Mapping.scale
      is `mat_spec.size` directly: BI sized GLOB textures in world units
      and our attribute coords *are* world units.
    - "ORCO" / "UV": TexCoord.Generated, the bbox-normalised substitute
      (we have no preserved UVs).  Mapping.scale = `mat_spec.size`,
      matching BI's per-axis cycles across the object bbox.

    `mat_spec.color`, when set, replaces the .blend's authored
    `diffuse_color` as the multiplier the image texture gets tinted
    by.  Push a summer-tinted image (e.g. snow blend's Hedge still
    has its summer green diffuse plus a brick image) toward a snow
    tint without losing the image's structural detail."""
    if mat_spec.color is not None:
        fallback_diffuse = (*mat_spec.color, 1.0)
    else:
        fallback_diffuse = tuple(m.diffuse_color)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = _bsdf_node(nt)
    tex_node = nt.nodes.new("ShaderNodeTexImage")
    tex_node.image = tex_img
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.vector_type = "POINT"
    mapping.inputs["Scale"].default_value = tuple(mat_spec.size)
    if any(mat_spec.ofs):
        mapping.inputs["Location"].default_value = tuple(mat_spec.ofs)
    if mat_spec.texco == "GLOB":
        coord = nt.nodes.new("ShaderNodeAttribute")
        coord.attribute_name = "blend_world_pos"
        nt.links.new(coord.outputs["Vector"], mapping.inputs["Vector"])
    else:
        coord = nt.nodes.new("ShaderNodeTexCoord")
        nt.links.new(coord.outputs["Generated"], mapping.inputs["Vector"])
    mul = nt.nodes.new("ShaderNodeMixRGB")
    mul.blend_type = "MULTIPLY"
    mul.inputs["Fac"].default_value = 1.0
    mul.inputs["Color2"].default_value = (*fallback_diffuse[:3], 1.0)
    nt.links.new(mapping.outputs["Vector"], tex_node.inputs["Vector"])
    nt.links.new(tex_node.outputs["Color"], mul.inputs["Color1"])
    nt.links.new(mul.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    m.diffuse_color = fallback_diffuse


def _build_noise_material(bpy, m, mat_spec=None) -> None:
    """CLOUDS substitute: Noise -> ColorRamp around the material's
    diffuse colour.  Used for `Material(noise=True)` entries -- BI's
    pre-2.5 procedural textures don't survive to modern Blender, and
    a noise band around the diffuse colour reads close enough at
    pakset zoom.

    `mat_spec.color`, when set, replaces the .blend's authored
    `diffuse_color` as the band's centre — needed for snow surfaces
    where BI's default CLOUDS slot paints white-over-diffuse but our
    extraction only carries the diffuse."""
    if mat_spec is not None and mat_spec.color is not None:
        fallback_diffuse = (*mat_spec.color, 1.0)[:4]
    else:
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


def _bind_textures_via_nodes(bpy, materials) -> None:
    """Build a node-graph substitute for each entry in `materials` (a
    `dict[str, pak.materials.Material]`); leave anything unlisted with
    `use_nodes=False` so Blender's auto-conversion paints the diffuse
    flat.  Names not present in `bpy.data.materials` raise -- a silent
    typo in the bake script's MATERIALS dict would render with the
    blend's stock colour and only diverge from sibling variants by a
    fixed offset.

    Must run after `_bake_world_into_meshes` so the `blend_world_pos`
    attribute the GLOB path samples is in place.

    See CLAUDE.md -> "Building-bake architecture" for the BI->EEVEE
    substitution context."""
    if not materials:
        return
    available = {m.name for m in bpy.data.materials}
    missing = set(materials) - available
    if missing:
        raise RuntimeError(
            f"MATERIALS targets unknown blend materials: {sorted(missing)}; "
            f"have {sorted(available)}"
        )
    for name, mat_spec in materials.items():
        m = bpy.data.materials[name]
        if mat_spec.slots is not None:
            _build_multislot_material(bpy, m, mat_spec)
            continue
        if mat_spec.image is not None:
            tex_img = _resolve_image(bpy, mat_spec.image)
            if tex_img is None:
                # Image data block referenced by the blend's MTex slot but
                # whose file 404'd from upstream (e.g. Britain's
                # `concrete-paving-smalll.jpg` typo'd Pavement path).
                # Fall back to flat diffuse rather than raising -- the
                # asset can still ship; tracked in TODO per-material.
                print(
                    f"  warning: MATERIALS['{name}'].image="
                    f"{mat_spec.image!r} did not load; falling back to "
                    "flat diffuse",
                    flush=True,
                )
                continue
            _build_image_material(bpy, m, tex_img, mat_spec)
        elif mat_spec.noise:
            _build_noise_material(bpy, m, mat_spec)


def _build_slot_output(bpy, nt, slot):
    """Build the per-slot sub-graph for one BI slot.  Returns a
    `(color_socket, intensity_socket)` pair where:

    - `color_socket` is the slot's RGB output (image pixels, or constant
      white for procedurals — BI's default Tex colour band).  Wired into
      the slot-stack MixRGB's Color2.
    - `intensity_socket` is the texture's per-pixel "influence" in [0,1]
      that BI multiplies into the slot's `colfac` before mixing.  For
      IMAGE textures this is the image's alpha (1.0 for opaque); for
      procedurals it's the noise value itself.  Wired (after multiply
      by `slot.fac`) into the MixRGB's Fac input — that's what makes
      a CLOUDS slot a *partial* overlay (lerping toward white where the
      noise is high) rather than a full replace.

    Returns `None, None` when the slot's image refused to load.

    Image slots: `<coord> -> Mapping(scale=size, ofs=ofs) -> ImageTexture
    -> Color/Alpha`.  Coord by texco — GLOB reads the `blend_world_pos`
    vertex attribute populated by `_bake_world_into_meshes` so the
    texture stays pinned to the .blend's world frame across per-facing
    rotations; ORCO / UV use `TexCoord.Generated`.

    Procedural slots: a `TexNoise` (CLOUDS / NOISE / MUSGRAVE all map
    to Blender's smooth fractal noise for our purposes) whose `Fac`
    output is the intensity (BI: noise value drives the influence
    factor; default texture colour at full influence is white).  Scale
    inversely tracks BI's `size` — BI doubles frequency by halving."""
    tex_img = None
    if slot.image is not None:
        tex_img = _resolve_image(bpy, slot.image)
        if tex_img is None:
            return None, None
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.vector_type = "POINT"
    mapping.inputs["Scale"].default_value = tuple(slot.size)
    if any(slot.ofs):
        mapping.inputs["Location"].default_value = tuple(slot.ofs)
    if slot.texco == "GLOB":
        coord = nt.nodes.new("ShaderNodeAttribute")
        coord.attribute_name = "blend_world_pos"
        nt.links.new(coord.outputs["Vector"], mapping.inputs["Vector"])
    else:
        coord = nt.nodes.new("ShaderNodeTexCoord")
        nt.links.new(coord.outputs["Generated"], mapping.inputs["Vector"])
    if slot.image is not None:
        tex_node = nt.nodes.new("ShaderNodeTexImage")
        tex_node.image = tex_img
        nt.links.new(mapping.outputs["Vector"], tex_node.inputs["Vector"])
        # Image texture: color from RGB, intensity from alpha.  For
        # opaque images alpha is 1.0 throughout so the mix factor is
        # just slot.fac — same as the previous single-slot path.
        return tex_node.outputs["Color"], tex_node.outputs["Alpha"]
    # Procedural: noise.Fac is the intensity (0..1) and feeds the slot's
    # influence factor.  Two output paths for the slot's RGB:
    #
    #   color_band -> intensity mapped through the band's stops via a
    #     ValToRGB node.  BI-faithful for Tex's with `TEX_COLORBAND` set
    #     (rare in the Britain pak).
    #
    #   else -> constant `slot.color` (from MTex.r/g/b).  BI's default
    #     when the texture supplies no RGB: Hedge's CLOUDS slot ships
    #     `(0.10, 0.06, 0.04)` and contributes a dark-brown overlay
    #     modulated by noise; MainColour1's ships `(0.60, 0.60, 0.60)`.
    #     Before this path landed the renderer emitted a black->white
    #     ramp here, dropping the per-slot tint and regressing summer
    #     dRGB on res_1600 when switched to slot form.
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 4.0
    noise.inputs["Detail"].default_value = 2.0
    nt.links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    if slot.color_band:
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        cr = ramp.color_ramp
        for i, (pos, r, g, b, a) in enumerate(slot.color_band):
            stop = cr.elements[i] if i < len(cr.elements) else cr.elements.new(pos)
            stop.position = pos
            stop.color = (r, g, b, a)
        nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
        return ramp.outputs["Color"], noise.outputs["Fac"]
    rgb_node = nt.nodes.new("ShaderNodeRGB")
    rgb_node.outputs[0].default_value = (*slot.color, 1.0)
    return rgb_node.outputs["Color"], noise.outputs["Fac"]


def _build_multislot_material(bpy, m, mat_spec):
    """Compose every entry in `mat_spec.slots` over the material's
    diffuse colour using each slot's blend mode + fac.  Mirrors BI's
    Tex stack: each slot's RGB output is mixed into the running base
    in declaration order; slot[N] sees the result of slot[0..N-1] as
    its base.

    A skipped slot (image 404, returns None from `_build_slot_output`)
    contributes nothing — the next slot mixes over the previous
    accumulated base.  `mat_spec.color`, when set, replaces the
    .blend's authored `diffuse_color` as the starting base."""
    if mat_spec.color is not None:
        base = (*mat_spec.color, 1.0)
    else:
        base = tuple(m.diffuse_color)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = _bsdf_node(nt)
    rgb_node = nt.nodes.new("ShaderNodeRGB")
    rgb_node.outputs[0].default_value = (*base[:3], 1.0)
    current = rgb_node.outputs["Color"]
    for slot in mat_spec.slots:
        slot_color, slot_intensity = _build_slot_output(bpy, nt, slot)
        if slot_color is None:
            continue
        mix = nt.nodes.new("ShaderNodeMixRGB")
        mix.blend_type = slot.blend
        nt.links.new(current, mix.inputs["Color1"])
        nt.links.new(slot_color, mix.inputs["Color2"])
        # MixRGB.Fac = slot.fac * texture_intensity.  Multiply via a
        # ShaderNodeMath so a CLOUDS slot's noise-Fac modulates the
        # influence (BI's `factor = colfac * intensity`).  For opaque
        # IMAGE slots this is `slot.fac * 1.0 = slot.fac` — equivalent
        # to wiring `slot.fac` directly, but uniform-path keeps the
        # graph shape consistent.
        fac_mul = nt.nodes.new("ShaderNodeMath")
        fac_mul.operation = "MULTIPLY"
        fac_mul.inputs[0].default_value = slot.fac
        nt.links.new(slot_intensity, fac_mul.inputs[1])
        nt.links.new(fac_mul.outputs["Value"], mix.inputs["Fac"])
        current = mix.outputs["Color"]
    nt.links.new(current, bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])


def _swap_to_id_map(bpy) -> dict[str, tuple[int, int, int]]:
    """Replace every material's node graph with a flat unlit emission of
    a unique RGB id.  Used by `--material-id-map`: the resulting render
    pixel-aligns with the normal render, and each material's pixels are
    identifiable by their exact RGB triple.

    Ids are spaced on a coarse grid (40-unit step in each channel,
    skipping (0,0,0)) so floating-point round-trip through the EEVEE /
    PNG encode survives — exact equality at integer RGB is reliable for
    flat emission, but a margin keeps it robust under future engine
    changes.  Returns the `{material_name: (r,g,b)}` mapping so the
    diagnostic driver can decode masks from the map PNG."""
    palette: list[tuple[int, int, int]] = []
    step = 40
    for r in range(step, 256, step):
        for g in range(step, 256, step):
            for b in range(step, 256, step):
                palette.append((r, g, b))
    mat_to_id: dict[str, tuple[int, int, int]] = {}
    for i, m in enumerate(bpy.data.materials):
        if i >= len(palette):
            raise RuntimeError(
                f"material-id-map: ran out of palette slots at {i} "
                f"({m.name})"
            )
        rgb = palette[i]
        mat_to_id[m.name] = rgb
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        emit = nt.nodes.new("ShaderNodeEmission")
        emit.inputs["Color"].default_value = (rgb[0] / 255.0, rgb[1] / 255.0,
                                              rgb[2] / 255.0, 1.0)
        emit.inputs["Strength"].default_value = 1.0
        nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
    return mat_to_id


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
    ortho_scale: float | None = None
    sun_energy: float | None = None


def strip_scene(bpy, strip_meshes: tuple[str, ...] | set[str] = ("Sphere",)) -> BlendAuthored:
    """Capture authored Camera/Sun parameters into a BlendAuthored, then
    remove the corresponding scene objects so the Viewpoint can install
    its own.  `strip_meshes` names extra mesh objects to drop on entry
    (default `("Sphere",)` -- upstream's sun-visualisation parent mesh;
    Lamp.001 is parented to it and goes via the LIGHT branch).  Also
    consumed by `pak/bake_way.py` -- ways install their own camera +
    sun from a Projection and discard the BlendAuthored return value."""
    authored = BlendAuthored()
    strip_names = set(strip_meshes)
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
        elif obj.name in strip_names:
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
    # Pin thread count for all engines: multi-threaded reduction order
    # is otherwise non-deterministic across CI runs even on identical
    # hardware.  Engine-specific determinism knobs go in
    # `_ENGINE_CONFIGURERS` below.
    scn.render.threads_mode = "FIXED"
    scn.render.threads = 1

    scn.render.engine = viewpoint.engine
    _ENGINE_CONFIGURERS[viewpoint.engine](scn)

    return cam, sun


def _configure_cycles(scn) -> None:
    """Pin Cycles knobs that are otherwise non-deterministic across CI
    runs even on identical hardware: adaptive sampling (per-pixel
    termination on a noise estimate), the denoiser (the blend may save
    it on), and the sample seed (the blend may save a non-zero value).
    Cross-CPU determinism (Intel vs AMD AVX2 transcendentals / embree)
    is still not guaranteed -- see CLAUDE.md -> CI."""
    scn.cycles.use_denoising = False
    scn.cycles.use_adaptive_sampling = False
    scn.cycles.seed = 0


def _configure_eevee(scn) -> None:
    """EEVEE substitute for BI: taa_render_samples=8 gives proper edge
    alpha-AA (1 writes 0-or-255 only and drops the edge ring); GTAO,
    bloom, SSR, volumetrics off for determinism across CI runners.
    World ambient defaults to 0.30 grey; per-asset Lighting overrides
    via `_apply_lighting`."""
    scn.eevee.taa_render_samples = 8
    scn.eevee.use_gtao = False
    scn.eevee.use_bloom = False
    scn.eevee.use_ssr = False
    scn.eevee.use_volumetric_lights = False
    scn.eevee.use_soft_shadows = False
    scn.eevee.use_shadow_high_bitdepth = True
    if scn.world is not None:
        scn.world.use_nodes = False
        try:
            scn.world.color = (0.30, 0.30, 0.30)
        except AttributeError:
            pass


def _apply_lighting(bpy, sun, authored, viewpoint, lighting) -> None:
    """Per-asset Lighting overrides applied on top of the Viewpoint +
    BlendAuthored defaults.  Called from `render_atlas` after
    `_install_camera_and_sun` and the engine configurer; each field is
    independently optional."""
    scn = bpy.context.scene
    if lighting.world_ambient is not None and scn.world is not None:
        try:
            scn.world.color = lighting.world_ambient
        except AttributeError:
            pass
    if lighting.sun_energy_scale is not None and authored.sun_energy is not None:
        sun.data.energy = authored.sun_energy * lighting.sun_energy_scale
    if (lighting.sun_elev_deg is not None or
            lighting.sun_az_offset_deg is not None):
        import math

        from pak.viewpoints import sun_rotation_for_camera
        elev = (lighting.sun_elev_deg if lighting.sun_elev_deg is not None
                else 30.0)
        az_off = (lighting.sun_az_offset_deg
                  if lighting.sun_az_offset_deg is not None else -90.0)
        # Recompute each facing's sun rotation in place against the override.
        for f in viewpoint.facings:
            cam_z_deg = math.degrees(f.camera_rotation_euler[2])
            f.sun_rotation_euler = sun_rotation_for_camera(
                cam_z_deg, sun_elev_deg=elev, sun_az_offset_deg=az_off,
            )


def configure_workbench(scn) -> None:
    """Flat-shading substitute: rendered pixel == material's diffuse
    colour directly.  No path tracing, no embree, no SIMD-sensitive
    reductions -- byte-stable across CPUs in practice.  Imported by
    `pak/bake_way.py` (ways have their own harness for composition
    reasons -- see CLAUDE.md -> "Way-bake architecture" -- but share
    the engine-config contract)."""
    shading = scn.display.shading
    shading.light = "FLAT"
    shading.color_type = "MATERIAL"
    shading.show_shadows = False
    shading.show_cavity = False
    shading.show_specular_highlight = False


_ENGINE_CONFIGURERS = {
    "CYCLES": _configure_cycles,
    "BLENDER_EEVEE": _configure_eevee,
    "BLENDER_WORKBENCH": configure_workbench,
}


def exit_edit_mode(bpy) -> None:
    """Upstream blends occasionally ship with one mesh stuck in edit
    mode (e.g. 4wheel-1850's body Cube.009).  Blender renders the BMesh
    edit buffer rather than `obj.data` until the object leaves edit
    mode -- our mesh.transform() / v.co writes are invisible to the
    renderer otherwise.  See CLAUDE.md -> "Edit-mode meshes".  Imported
    by `pak/bake_way.py`."""
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

    exit_edit_mode(bpy)

    cache: dict = {}
    def renders(obj):
        return (not obj.hide_render
                and all(_collection_renders(bpy, c, cache) for c in obj.users_collection))

    rendered = [o for o in scn.objects if o.type == "MESH" and renders(o)]

    # Several upstream `-snow.blend` siblings (e.g. `citybuildings/
    # 1600-detatched-house-2f-snow.blend`) ship with their geometry
    # collection set to `hide_render=True` — JP toggles visibility
    # manually before rendering interactively, and the saved state
    # carries the off-toggle.  When the per-collection filter rejects
    # every mesh, lift `hide_render` on every collection containing a
    # mesh whose own `hide_render` is False — Blender's renderer
    # itself respects collection.hide_render regardless of our vertex
    # transforms, so we have to flip the flag, not just the filter.
    # Same principle as the film_transparent / RGBA forcing in
    # `_install_camera_and_sun`: don't trust the blend's saved state
    # when it's the engine-substitute-default we know is wrong.
    if not rendered:
        for c in bpy.data.collections:
            if any(o.type == "MESH" and not o.hide_render for o in c.objects):
                c.hide_render = False
        cache.clear()
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
        # Snapshot blend-frame world position as a vertex attribute so
        # the shader can sample BI's TEXCO_GLOB coords directly after
        # `_apply_facing` rewrites v.co per facing.  Per-facing rotation
        # otherwise wobbles Generated-derived texture coords because the
        # mesh AABB grows with rotation; reading from this attribute
        # keeps the texture pinned to the original blend frame, the way
        # BI did when only the camera moved.
        mesh = obj.data
        attr = mesh.attributes.get("blend_world_pos")
        if attr is None:
            attr = mesh.attributes.new(
                name="blend_world_pos", type="FLOAT_VECTOR", domain="POINT",
            )
        attr.data.foreach_set("vector", [c for v in orig for c in v])
        records.append((obj, orig))

    # Force the matrix_world cache to refresh: assignments to
    # matrix_basis are lazy, and the renderer otherwise reads stale
    # non-identity matrices for objects with non-unit scale,
    # double-applying their original transform on top of the baked mesh.
    bpy.context.view_layer.update()
    return records


def _compute_fit(mathutils, records, fit_kind: str,
                 blend_ortho: float | None = None):
    """Build the world->fitted-frame 4x4 the per-facing transform composes
    over.

    `fit_kind="none"` -- identity (model renders at native blend-coord
    scale).  Used by the square calibration view, where upstream camera
    positions are in blend coords.

    `fit_kind="hex"` -- scale by `2 * HEX_TILE_RADIUS / blend_ortho` to
    convert blend coords -> intra-tile coords; no XY recentre, no
    z-floor drop.  The artist's authored XYZ placement is the contract
    -- same as upstream's BI render reads it.  Vehicles authored
    near origin and at z>=0 (the upstream contributing-graphics spec)
    sit centred in the cell; assets that aren't surface that as a
    real authoring quirk rather than have it masked by our recentre.

    `blend_ortho` is the blend's authored ortho_scale read by
    `strip_scene` -- falls back to `UPSTREAM_ORTHO_SCALE` (24,
    vehicle-blend convention) when the blend has no camera.  Buildings
    tend to ship at ortho_scale=12 (twice the per-cell zoom); honouring
    that per-asset is what makes them render at upstream's per-pixel
    scale instead of half-size."""
    M = mathutils.Matrix
    if fit_kind == "none":
        return M.Identity(4)
    if fit_kind == "hex":
        from pak.hex_synth import HEX_TILE_RADIUS, UPSTREAM_ORTHO_SCALE  # noqa: E402
        ortho = blend_ortho if blend_ortho is not None else UPSTREAM_ORTHO_SCALE
        scale = 2.0 * HEX_TILE_RADIUS / ortho
        return M.Diagonal((scale, scale, scale, 1.0))
    raise SystemExit(f"unknown fit_kind: {fit_kind!r}")


def _apply_facing(records, M_target) -> None:
    """Rewrite each mesh's vertices to `M_target @ canonical_world_co`.
    Called once per facing; matrix_world stays the identity."""
    for obj, orig in records:
        for v, oc in zip(obj.data.vertices, orig, strict=True):
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
                 name: str, cols_per_row: int | None = None,
                 keep_per_facing: bool = False,
                 materials: dict | None = None,
                 lighting=None,
                 material_id_map: bool = False) -> None:
    """Render `viewpoint.facings` of the currently loaded blend.  Writes
    `<out_dir>/<name>.png` (atlas).  With `keep_per_facing=True`, also
    writes `<out_dir>/<name>_<label>.png` per facing -- used by the
    calibration diff against the upstream pak.

    `materials` is the per-asset `MATERIALS = {...}` dict from the bake
    script (a `dict[str, pak.materials.Material]`).  Applied after the
    world-bake step so the GLOB-coord path can read the
    `blend_world_pos` vertex attribute it populates.

    `material_id_map=True` replaces every material with a flat unlit
    emission of a unique RGB id (sidecar JSON written next to the atlas)
    so the resulting render pixel-aligns with the normal pass but each
    material's coverage is identifiable.  Used by `pak.diag_per_material`
    to attribute the upstream-vs-ours dRGB to specific materials."""
    import json

    import numpy as np

    authored = strip_scene(bpy, viewpoint.strip_meshes)
    if viewpoint.engine == "BLENDER_EEVEE":
        _reload_external_textures(bpy)
    cam, sun = _install_camera_and_sun(bpy, viewpoint, authored)
    if lighting is not None:
        _apply_lighting(bpy, sun, authored, viewpoint, lighting)
    records = _bake_world_into_meshes(bpy, mathutils)
    if material_id_map:
        mat_to_id = _swap_to_id_map(bpy)
        sidecar = Path(out_dir) / f"{name}.materials.json"
        sidecar.parent.mkdir(parents=True, exist_ok=True)
        sidecar.write_text(json.dumps(mat_to_id, indent=2, sort_keys=True))
    elif viewpoint.engine == "BLENDER_EEVEE" and materials:
        _bind_textures_via_nodes(bpy, materials)
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
            M_scale = mathutils.Matrix.Diagonal((
                facing.model_scale, facing.model_scale, facing.model_scale, 1.0,
            ))
            M_target = (extrinsic
                        @ mathutils.Matrix.Translation(facing.model_translation)
                        @ M_scale
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
                    choices=["hex", "square", "hex_building", "square_building",
                             "fence_square", "tree_hex", "tree_square"])
    ap.add_argument("--tree-grid", default=None,
                    help="AGES,SEASONS — grid size for viewpoint=tree_hex/"
                         "tree_square; SEASONS controls leaf-colour overrides "
                         "(currently summer only; expand when the rest are "
                         "calibrated)")
    ap.add_argument("--keep-per-facing", action="store_true",
                    help="write per-facing PNGs alongside the atlas (used by diff)")
    ap.add_argument("--cols-per-row", type=int, default=None)
    ap.add_argument("--building-footprint", default=None,
                    help="X,Y,L,H — footprint (dims_x, dims_y, layouts, "
                         "heights) for viewpoint=hex_building or "
                         "square_building; required for those modes")
    ap.add_argument("--materials", default="",
                    help="JSON serialisation of the bake script's "
                         "`MATERIALS = {...}` dict (see pak.materials).  "
                         "Per-material image/noise/texco/size descriptions "
                         "the renderer wires into Principled BSDF node "
                         "graphs; unlisted materials render flat-diffuse.")
    ap.add_argument("--lighting", default="",
                    help="JSON serialisation of the bake script's optional "
                         "`LIGHTING = Lighting(...)` block; per-asset world-"
                         "ambient + sun overrides.  See pak.materials.Lighting.")
    ap.add_argument("--material-id-map", action="store_true",
                    help="Diagnostic: instead of the normal render, "
                         "replace every material with a flat unlit "
                         "emission of a unique RGB id, write a "
                         "`<name>.materials.json` sidecar mapping name → "
                         "RGB.  Resulting atlas pixel-aligns with the "
                         "normal render; consumers (`pak.diag_per_material`) "
                         "use the id map to extract per-material masks.")
    return ap.parse_args(argv)


def main(argv):
    import bpy
    import mathutils

    from pak.viewpoints import (
        HEX_VIEWPOINT,
        SQUARE_VIEWPOINT,
        building_hex_viewpoint,
        building_square_viewpoint,
        fence_square_viewpoint,
        tree_hex_viewpoint,
        tree_square_viewpoint,
    )

    args = _parse_args(argv)
    if args.viewpoint == "hex":
        vp = HEX_VIEWPOINT
    elif args.viewpoint == "square":
        vp = SQUARE_VIEWPOINT
    elif args.viewpoint == "fence_square":
        vp = fence_square_viewpoint()
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
    elif args.viewpoint in ("tree_hex", "tree_square"):
        if not args.tree_grid:
            raise SystemExit(
                f"--viewpoint {args.viewpoint} requires --tree-grid AGES,SEASONS"
            )
        ages, seasons = (int(s) for s in args.tree_grid.split(","))
        factory = (tree_hex_viewpoint if args.viewpoint == "tree_hex"
                   else tree_square_viewpoint)
        vp = factory(ages=ages, seasons=seasons)
    else:
        raise SystemExit(f"unknown viewpoint: {args.viewpoint!r}")

    materials = None
    if args.materials:
        import json

        from pak.materials import from_jsonable
        materials = from_jsonable(json.loads(args.materials))

    lighting = None
    if args.lighting:
        import json

        from pak.materials import Lighting
        lighting = Lighting.from_jsonable(json.loads(args.lighting))

    render_atlas(bpy, mathutils, vp, args.out, args.name,
                 cols_per_row=args.cols_per_row,
                 keep_per_facing=args.keep_per_facing,
                 materials=materials,
                 lighting=lighting,
                 material_id_map=args.material_id_map)
    return 0


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(argv))
