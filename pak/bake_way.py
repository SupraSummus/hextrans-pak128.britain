"""Bake a hex-way atlas from an upstream blend.

See CLAUDE.md → "Way-bake architecture" for the contract: the upstream
blend is the geometric atom; this driver scales it onto a hex
through-tile chord, then for each of the 63 hex ribis composes the
atom along the path segments emitted by `pak/way_topology.py` (stubs,
chords, V-bend legs, junctions = pairwise chords), bisects each clone
at its cap planes + the hex outline, applies the engine's hex
projection shear, and renders one PNG per ribi through Cycles.  The
per-ribi PNGs are stitched into a single atlas in the same popcount-
then-ribi order as `pak.way.HEX_ENTRIES`.

Run via:

    blender -b -P pak/bake_way.py -- \\
        --blend ways/ns-cssr.blend --name cssr --out ways/

`--blend` is resolved against the blends repo via `pak/fetch_blend.py`;
the actual file is fetched on demand and cached.

Blender-only — this module imports `bpy` and `mathutils` at top level
and isn't importable outside `blender -b -P`.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from pathlib import Path

import bmesh
import bpy
import mathutils
import numpy as np


HERE = Path(__file__).resolve().parent
# Put the repo root on sys.path so `pak.<module>` imports resolve.
# `way_topology` uses `from .way import …`, so we need the package form,
# not a flat sys.path on the `pak/` dir.
sys.path.insert(0, str(HERE.parent))

from pak.fetch_blend import fetch as fetch_blend  # noqa: E402
from pak.hex_synth import DEFAULT_W  # noqa: E402
from pak.way_proj import PROJECTIONS, Projection  # noqa: E402
from pak.way_topology import (  # noqa: E402
    atom_offsets_along_path, cap_plane, path_chord_angle,
    path_chord_length, path_chord_midpoint, path_chord_unit,
)


def _argv() -> list[str]:
    """Return the script args after `--` (Blender swallows everything before)."""
    if "--" in sys.argv:
        return sys.argv[sys.argv.index("--") + 1:]
    return []


def _parse(args: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--blend", required=True,
                   help="blend path within the blends repo, e.g. ways/ns-cssr.blend")
    p.add_argument("--name", required=True,
                   help="output basename (atlas <name>.png)")
    p.add_argument("--out", type=Path, required=True,
                   help="output directory (atlas PNG goes here)")
    # Default-strip: `Sphere` is the upstream sun-direction visualizer
    # (`pak/render.py` strips it for vehicle bakes for the same
    # reason).  `Plane` is NOT noise in ns-cssr.blend — it's the
    # 2048-poly ballast pile.  Per-blend strip lists move into a
    # `ways/<asset>.py` wrapper once the asset count grows past 1.
    p.add_argument("--strip", default="Sphere",
                   help="comma-separated mesh object names to strip "
                        "(default: 'Sphere'). All cameras + lights "
                        "are always stripped.")
    p.add_argument("--samples", type=int, default=32,
                   help="Cycles samples per cell (default 32).")
    p.add_argument("--only", default="",
                   help="comma-separated ribi labels to bake; the rest "
                        "are zero-filled.  Default: all entries.")
    p.add_argument("--projection", choices=tuple(PROJECTIONS), default="hex",
                   help="hex (default, production) or square "
                        "(upstream-diff calibration)")
    p.add_argument("--cell-dir", type=Path, default=None,
                   help="directory for per-cell debug PNGs.  Default: a "
                        "temp dir cleaned up on exit (only the stitched "
                        "atlas lands in --out).")
    p.add_argument("--materials", default="",
                   help="JSON dict mapping material-name -> [r, g, b] 0..255. "
                        "Applied to the blend's materials by name after open, "
                        "before render.  Lets one blend (e.g. ns-cssr.blend) "
                        "serve the entire rail-grade catalog by recolouring "
                        "four materials per variant.  The per-rail bake "
                        "script `ways/<rail>.py` holds the calibrated values "
                        "inline as `MATERIALS = {...}` and passes them "
                        "through `bake_way_main(..., materials=MATERIALS)`.")
    return p.parse_args(args)


def _apply_material_overrides(
    overrides: dict[str, list[int]],
) -> None:
    """Set `mat.diffuse_color` for every named material that exists in the
    open blend.  Unknown names raise — a silent typo would render with
    the blend's stock colour and look fine in isolation, only diverging
    from sibling variants by the wrong fixed offset.

    `overrides` arrives via `json.loads` from `--materials`, so JSON
    rules apply: the inner sequences come through as `list[int]` (the
    parent driver passes tuples but JSON has no tuple type).  Anything
    three-element-and-iterable works because the loop body just
    unpacks `(r, g, b)`.

    Old-style (`use_nodes=False`) materials render via `diffuse_color`
    directly under Cycles' auto-conversion; `ns-cssr.blend`'s materials
    are all `use_nodes=False`.  If a future blend ships node-graph
    materials, this would need to find and update a Principled BSDF
    Base Color input instead.
    """
    available = {m.name for m in bpy.data.materials}
    missing = set(overrides) - available
    if missing:
        raise RuntimeError(
            f"--materials targets unknown blend materials: {sorted(missing)}; "
            f"have {sorted(available)}"
        )
    for name, (r, g, b) in overrides.items():
        bpy.data.materials[name].diffuse_color = (
            r / 255.0, g / 255.0, b / 255.0, 1.0,
        )


# Materials whose carrier meshes are dropped on every bake regardless
# of caller intent.  Upstream way blends ship a `Transparent` material
# on a flat ground plane (`ns-cssr.blend`'s `Plane.005`) that was meant
# to be invisible — diffuse 0.8 grey, no texture wired up.  Cycles
# renders it as opaque mid-grey, contaminating ~50 % of the bake's lit
# pixels with a fake ground that upstream's atlases don't show.  Strip
# by material name rather than mesh name: `Plane.005` is an incidental
# Blender autosuffix that can shift on re-save, but `Transparent`
# names the artist's intent.
_STRIP_MATERIALS: frozenset[str] = frozenset({"Transparent"})


def _strip_scene(strip_meshes: set[str]) -> None:
    """Strip every camera/light, any mesh whose name is in
    `strip_meshes`, and any mesh carrying a material in
    `_STRIP_MATERIALS`.  Cameras + lights always go — we install our
    own from the way-bake recipe."""
    for obj in list(bpy.context.scene.objects):
        if obj.type in ("CAMERA", "LIGHT"):
            bpy.data.objects.remove(obj, do_unlink=True)
            continue
        if obj.type != "MESH":
            continue
        if obj.name in strip_meshes:
            bpy.data.objects.remove(obj, do_unlink=True)
            continue
        if any(s.material and s.material.name in _STRIP_MATERIALS
               for s in obj.material_slots):
            bpy.data.objects.remove(obj, do_unlink=True)


def _atoms() -> list:
    """Return every MESH object remaining in the scene, sorted by name.
    Stable ordering for readability of the per-bake stdout — Cycles
    sampling still randomises pixel output run-to-run."""
    return sorted(
        (obj for obj in bpy.context.scene.objects if obj.type == "MESH"),
        key=lambda o: o.name,
    )


def _bake_world_transforms(atoms) -> None:
    """Bake `obj.matrix_world` into the mesh's vertex data and reset
    the world matrix to identity, so subsequent `mesh.transform()`
    calls compose cleanly without re-decomposing the basis (CLAUDE.md
    "matrix_basis drops shear")."""
    for obj in atoms:
        # Edit-mode landmine: writes to obj.data.vertices are invisible
        # to the renderer if the mesh is in edit mode.  Force OBJECT.
        if obj.data.is_editmode:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="OBJECT")
        obj.data.transform(obj.matrix_world)
        obj.matrix_world = mathutils.Matrix.Identity(4)


def _y_extent(atoms) -> tuple[float, float]:
    """Y range across every vertex of every atom.  The blend authors the
    rail along +Y; this is the chord direction the atom occupies."""
    y_min = min(v.co.y for obj in atoms for v in obj.data.vertices)
    y_max = max(v.co.y for obj in atoms for v in obj.data.vertices)
    return y_min, y_max


def _scale_uniform(atoms, scale: float) -> None:
    """Multiply every atom's mesh by `scale` uniformly in XYZ.  Uniform
    (not just Y) because cross-section sizes (rail gauge, sleeper width,
    ballast thickness) share the blend's world scale; squashing one
    axis independently would distort the rail's aspect ratio."""
    if scale == 1.0:
        return
    m = mathutils.Matrix.Diagonal((scale, scale, scale, 1.0))
    for obj in atoms:
        obj.data.transform(m)


def _centre_y(atoms, *, y_min: float, y_max: float) -> None:
    """Shift every atom along -Y so the Y extent is centred on origin."""
    y_mid = (y_min + y_max) * 0.5
    if y_mid == 0.0:
        return
    m = mathutils.Matrix.Translation((0.0, -y_mid, 0.0))
    for obj in atoms:
        obj.data.transform(m)


def _install_camera_and_sun(projection: Projection) -> None:
    """Add the projection's camera + sun.  For hex this is the engine
    camera looking +Y with ortho_scale = 2R; for square it's
    `SQUARE_VIEWPOINT['S']` verbatim (the upstream `vehicles`-alignment
    'S' facing — see `pak/viewpoints.py` for the cross-pakset
    convention)."""
    scene = bpy.context.scene

    cam_data = bpy.data.cameras.new("_way_camera")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = projection.ortho_scale
    cam_obj = bpy.data.objects.new("_way_camera_obj", cam_data)
    scene.collection.objects.link(cam_obj)
    cam_obj.location = projection.camera_location
    cam_obj.rotation_euler = projection.camera_rotation_euler
    scene.camera = cam_obj

    sun_data = bpy.data.lights.new("_way_sun", type="SUN")
    sun_data.energy = 0.028  # matches viewpoints.py _SUN_ENERGY
    sun_obj = bpy.data.objects.new("_way_sun_obj", sun_data)
    scene.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = projection.sun_rotation_euler


def _configure_render(*, image_width: int, samples: int) -> None:
    """Force RGBA + transparent film, fixed resolution, Cycles backend.
    Overrides whatever the blend saved (some Britain blends ship with
    RGB + solid world background)."""
    scene = bpy.context.scene
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = True
    scene.render.resolution_x = image_width
    # Match the hex cell shape: W wide × W tall (2u + top_pad = 4u = W
    # at the standard W=128 / u=32 / top_pad=4*lift=4*16=64 settings).
    scene.render.resolution_y = image_width
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples


def _clone_atom(template, *, name_suffix: str):
    """Return a new mesh object whose mesh data is a deep copy of
    `template.data`.  Linked to the active collection so it participates
    in the next render."""
    mesh = template.data.copy()
    mesh.name = f"{template.data.name}_{name_suffix}"
    obj = bpy.data.objects.new(f"{template.name}_{name_suffix}", mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def _bisect_mesh(mesh, plane_co: tuple[float, float, float],
                 plane_no: tuple[float, float, float]) -> None:
    """Bisect `mesh` against the plane defined by `(plane_co, plane_no)`,
    removing the half-space opposite the normal direction.  No-op on
    empty meshes."""
    if len(mesh.vertices) == 0:
        return
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        # bmesh.ops.bisect_plane: `clear_inner` removes the negative
        # side (opposite the normal); `clear_outer` removes the positive
        # side (along the normal).  We construct every plane normal to
        # point inward (toward the chord midpoint / hex centre), so the
        # kept half is the +normal side — that means `clear_inner=True`.
        bmesh.ops.bisect_plane(
            bm,
            geom=list(bm.verts) + list(bm.edges) + list(bm.faces),
            plane_co=plane_co,
            plane_no=plane_no,
            clear_inner=True,
            clear_outer=False,
        )
        bm.to_mesh(mesh)
    finally:
        bm.free()


def _place_atom_along_path(obj, path, *, chord_offset: float = 0.0) -> None:
    """Bake the per-path transform onto the mesh's vertex data.

    The atom is authored along +Y, centred at origin (post scale +
    centre_y).  Rotate it around Z so its +Y axis lines up with the
    chord direction, then translate so its centre lands at
    `chord_midpoint + chord_offset * chord_dir`.  Multi-atom-per-path
    tiling threads a list of `chord_offset` values from
    `atom_offsets_along_path` (one atom per slot along the chord);
    `chord_offset=0` places the atom centred on the chord midpoint.
    Atoms overrunning the chord ends are trimmed by `_apply_caps`.
    """
    angle = path_chord_angle(path)
    mx, my = path_chord_midpoint(path)
    ux, uy = path_chord_unit(path)
    cx = mx + chord_offset * ux
    cy = my + chord_offset * uy
    m = (mathutils.Matrix.Translation((cx, cy, 0.0))
         @ mathutils.Matrix.Rotation(angle, 4, "Z"))
    obj.data.transform(m)


def _bisect_against_xy_planes(obj, planes_xy) -> None:
    """Bisect `obj.data` against a sequence of vertical planes, each
    given as `((co_x, co_y), (no_x, no_y))` in world XY.  The plane
    contains the world Z axis (extruded vertically), which matches both
    the per-path cap planes and the tile-outline planes — the only
    bisects the way bake driver needs."""
    for (cx, cy), (nx, ny) in planes_xy:
        _bisect_mesh(obj.data,
                     plane_co=(cx, cy, 0.0),
                     plane_no=(nx, ny, 0.0))


def _apply_caps(obj, path) -> None:
    """Bisect the per-path clone at both cap planes (skipping V-bend
    apex caps marked `skip_cap_*`)."""
    planes = (cap_plane(path, end) for end in ("a", "b"))
    _bisect_against_xy_planes(obj, (p for p in planes if p is not None))


def _clip_to_outline(obj, projection: Projection) -> None:
    """Bisect against all tile-edge planes so the composed mesh sits
    inside the tile silhouette.  Catches atoms whose authored ground
    plane reaches past the tile corners (ns-cssr's `Plane.005` is the
    standing example under hex; the same plane sits well inside the
    larger square tile and is a no-op there)."""
    _bisect_against_xy_planes(obj, projection.clip_planes())


def _apply_extrinsic_to(obj, extrinsic_rows) -> None:
    m = mathutils.Matrix(extrinsic_rows)
    obj.data.transform(m)


def _render_to(out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.render.filepath = str(out_path)
    bpy.ops.render.render(write_still=True)


def _read_png(path: Path) -> np.ndarray:
    """Load an RGBA PNG via Blender's image loader (already a dep), return
    a (H, W, 4) uint8 array, origin top-left."""
    img = bpy.data.images.load(str(path), check_existing=False)
    try:
        w, h = img.size
        # `image.pixels` is a flat RGBA float buffer, bottom-up.
        pix = np.array(img.pixels[:], dtype=np.float32).reshape((h, w, 4))
        pix = np.flipud(pix)
        return (np.clip(pix, 0.0, 1.0) * 255.0 + 0.5).astype(np.uint8)
    finally:
        bpy.data.images.remove(img)


def _save_png(path: Path, atlas: np.ndarray) -> None:
    """Write an (H, W, 4) uint8 array as RGBA PNG via Blender's image
    saver (avoids needing PIL inside the bake)."""
    h, w, _ = atlas.shape
    img = bpy.data.images.new(name=path.stem, width=w, height=h, alpha=True)
    try:
        flat = np.flipud(atlas).astype(np.float32) / 255.0
        img.pixels = flat.reshape(-1).tolist()
        img.filepath_raw = str(path)
        img.file_format = "PNG"
        img.save()
    finally:
        bpy.data.images.remove(img)


def _stitch_atlas(projection: Projection, cell_paths: dict[str, Path],
                  cell_size: int) -> np.ndarray:
    """Compose an atlas from per-cell PNGs in the projection's entries
    order plus the `-` (no-way) slot at the front.  Missing entries
    are zero-filled (transparent).

    Row = index // cols, col = index % cols.  Hex uses 8 cols
    (popcount-major: row 0 = `-` + 6 singletons; row 7 = the 6-way
    junction).  Square uses 4 cols (one row per popcount: row 0 = `-`
    + N/S/E, row 1 = W + 3 pairs, …).
    """
    labels = ["-"] + [label for label, _ in projection.entries]
    cols = projection.atlas_cols
    n = len(labels)
    rows = (n + cols - 1) // cols
    atlas = np.zeros((rows * cell_size, cols * cell_size, 4), dtype=np.uint8)
    for idx, label in enumerate(labels):
        path = cell_paths.get(label)
        if path is None:
            continue
        cell = _read_png(path)
        if cell.shape != (cell_size, cell_size, 4):
            raise RuntimeError(
                f"cell {label}: expected {cell_size}x{cell_size} RGBA, "
                f"got {cell.shape}")
        r, c = divmod(idx, cols)
        atlas[r * cell_size:(r + 1) * cell_size,
              c * cell_size:(c + 1) * cell_size] = cell
    return atlas


def _bake_one_cell(templates, *, label: str, edges: tuple[str, ...],
                   atom_step: float, projection: Projection,
                   out_path: Path) -> None:
    """Compose the atom along every path for this ribi, bisect, render
    one cell PNG, then tear the clones down.

    `atom_step` is the atom's post-scale Y-extent — the step between
    consecutive atoms when a chord needs multiple atoms tiled to stay
    continuous.  Applies to both projections: hex's `1/12` conversion
    makes the atom short relative to the hex chord, and square's
    native blend atom is similarly short relative to the upstream
    square chord (one strand ≈ 8.78 blend units, NS chord = 2 *
    SQUARE_TILE_HALF = 24).  Outer atoms overrun the chord ends; the
    cap bisect trims them.
    """
    # 1. Hide originals from render (we render the clones).
    for t in templates:
        t.hide_render = True

    clones: list = []
    paths = projection.for_edges_paths(edges)

    # 2. For each path, tile atoms along the chord, transform + cap +
    # silhouette-clip each clone.
    for pi, path in enumerate(paths):
        offsets = atom_offsets_along_path(path_chord_length(path), atom_step)
        for ai, offset in enumerate(offsets):
            for t in templates:
                obj = _clone_atom(t, name_suffix=f"{label}_p{pi}_a{ai}")
                _place_atom_along_path(obj, path, chord_offset=offset)
                _apply_caps(obj, path)
                _clip_to_outline(obj, projection)
                clones.append(obj)

    # 3. Apply the projection shear (hex only — square uses identity)
    # to every clone so the camera reproduces the engine's pixels.
    if projection.extrinsic is not None:
        for obj in clones:
            _apply_extrinsic_to(obj, projection.extrinsic)

    # 4. Render.
    _render_to(out_path)

    # 5. Tear down clones; restore the templates' render visibility for
    # the next cell.  (Templates stay at their post-scale, pre-shear
    # state — we never mutate their mesh data during composition.)
    for obj in clones:
        mesh = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.meshes.remove(mesh)
    for t in templates:
        t.hide_render = False


def main() -> None:
    args = _parse(_argv())
    projection = PROJECTIONS[args.projection]

    blend_path = fetch_blend(args.blend)
    print(f"loading blend: {blend_path}  projection={projection.name}")
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))

    # 0. Apply per-variant material colour overrides (rail-grade
    # recolour catalog).  Done before scene stripping so it errors out
    # on a typo even when the override targets a material whose only
    # carrier mesh would otherwise be stripped.
    if args.materials:
        _apply_material_overrides(json.loads(args.materials))

    # 1. Strip authored cameras + lights, plus caller-named meshes.
    _strip_scene({n for n in args.strip.split(",") if n})
    templates = _atoms()
    print(f"atoms after strip: {[a.name for a in templates]}")

    # 2. Bake matrix_world into mesh data so subsequent transforms
    # compose cleanly.
    _bake_world_transforms(templates)

    # 3. Apply the projection's uniform atom scale (hex: 1/12 blend ->
    # intra-tile conversion; square: native blend coords) and centre
    # the atom on origin so multi-atom tiling positions atoms
    # symmetrically around the chord midpoint.  `atom_step` (the
    # post-scale Y-extent) drives the multi-atom-per-chord tiling in
    # `_bake_one_cell`; both projections tile (the blend's atom is
    # shorter than the chord in both intra-tile and blend coords —
    # upstream's NS cell visibly contains more sleepers than one
    # atom holds).
    y_min, y_max = _y_extent(templates)
    if projection.atom_scale is not None:
        _scale_uniform(templates, projection.atom_scale)
        y_min *= projection.atom_scale
        y_max *= projection.atom_scale
    _centre_y(templates, y_min=y_min, y_max=y_max)
    atom_step = y_max - y_min
    print(f"rail Y extent [{y_min:.3f}, {y_max:.3f}] "
          f"(scale={projection.atom_scale}, atom_step={atom_step:.3f})")

    # 4. Camera + sun + render config from the projection.
    _install_camera_and_sun(projection)
    _configure_render(image_width=DEFAULT_W, samples=args.samples)

    # 5. Per-ribi composition + render.  Each cell writes one PNG to
    # `cell_dir`; `_stitch_atlas` reads them back to compose the
    # output atlas.
    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    cell_dir: Path
    cell_dir_owned: tempfile.TemporaryDirectory | None = None
    if args.cell_dir is not None:
        cell_dir = args.cell_dir
        cell_dir.mkdir(parents=True, exist_ok=True)
    else:
        cell_dir_owned = tempfile.TemporaryDirectory(prefix="bake_way_")
        cell_dir = Path(cell_dir_owned.name)

    only = {s for s in args.only.split(",") if s}
    cell_paths: dict[str, Path] = {}
    try:
        for label, edges in projection.entries:
            if only and label not in only:
                continue
            cell_path = cell_dir / f"{args.name}_{label}.png"
            print(f"baking ribi {label} edges={edges} -> {cell_path.name}")
            _bake_one_cell(templates, label=label, edges=edges,
                           atom_step=atom_step, projection=projection,
                           out_path=cell_path)
            cell_paths[label] = cell_path

        # 6. Stitch the atlas.
        atlas_path = out_dir / f"{args.name}.png"
        atlas = _stitch_atlas(projection, cell_paths, cell_size=DEFAULT_W)
        _save_png(atlas_path, atlas)
        print(f"wrote atlas {atlas_path} "
              f"({atlas.shape[1]}x{atlas.shape[0]}, {len(cell_paths)} cells)")
    finally:
        if cell_dir_owned is not None:
            cell_dir_owned.cleanup()


if __name__ == "__main__":
    main()
