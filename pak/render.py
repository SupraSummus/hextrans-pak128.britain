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
sys.path.insert(0, str(HERE))


@dataclass
class Facing:
    """One sprite direction within a Viewpoint."""
    label: str
    camera_location: tuple[float, float, float]
    camera_rotation_euler: tuple[float, float, float]  # radians
    sun_rotation_euler: tuple[float, float, float]  # radians
    model_rot_z_deg: float = 0.0  # rotation applied to the mesh after fit


@dataclass
class Viewpoint:
    """Self-contained recipe for rendering one asset N ways."""
    name: str
    image_width: int
    ortho_scale: float
    sun_energy: float
    fit_kind: str  # "hex" (centre + z_floor + 1/12 scale) or "none" (identity)
    extrinsic: Optional[tuple]  # 4x4 row-major tuple, or None for identity
    facings: list[Facing]


def _strip_scene(bpy) -> None:
    """Remove any pre-existing cameras, lights, and the upstream
    `Sphere` sun visualisation.  The blend is treated as model data;
    every render-time prop is created fresh from the Viewpoint."""
    for obj in list(bpy.context.scene.objects):
        if obj.type in ("CAMERA", "LIGHT") or obj.name == "Sphere":
            bpy.data.objects.remove(obj, do_unlink=True)


def _install_camera_and_sun(bpy, viewpoint: Viewpoint):
    """Create one camera and one SUN light, configured per the Viewpoint.
    Per-facing pose changes (location, rotation) happen in the render loop."""
    cam_data = bpy.data.cameras.new("_render_camera")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = viewpoint.ortho_scale
    cam = bpy.data.objects.new("_render_camera", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.rotation_mode = "XYZ"

    sun_data = bpy.data.lights.new("_render_sun", type="SUN")
    sun_data.energy = viewpoint.sun_energy
    sun = bpy.data.objects.new("_render_sun", sun_data)
    bpy.context.scene.collection.objects.link(sun)
    sun.rotation_mode = "XYZ"

    scn = bpy.context.scene
    scn.render.resolution_x = viewpoint.image_width
    scn.render.resolution_y = viewpoint.image_width
    scn.render.resolution_percentage = 100
    scn.render.film_transparent = True
    scn.render.image_settings.color_mode = "RGBA"

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


def _compute_fit(mathutils, records, fit_kind: str):
    """Build the world->fitted-frame 4x4 the per-facing transform composes
    over.  `fit_kind="none"` is identity (model renders at its native
    scale).  `fit_kind="hex"` centres the XY bounding box on origin,
    drops the lowest visible vertex to z=0, and scales by the pakset-wide
    blend->hex ratio (2R / upstream_ortho_scale)."""
    M = mathutils.Matrix
    if fit_kind == "none":
        return M.Identity(4)
    if fit_kind == "hex":
        from hex_synth import HEX_TILE_RADIUS, UPSTREAM_ORTHO_SCALE  # noqa: E402
        scale = (2.0 * HEX_TILE_RADIUS) / UPSTREAM_ORTHO_SCALE
        xs = []; ys = []; zs = []
        for _, orig in records:
            for c in orig:
                xs.append(c.x); ys.append(c.y); zs.append(c.z)
        if not xs:
            raise SystemExit("no renderable mesh vertices to fit")
        cx = (min(xs) + max(xs)) / 2.0
        cy = (min(ys) + max(ys)) / 2.0
        z_floor = min(zs)
        return M.Scale(scale, 4) @ M.Translation((-cx, -cy, -z_floor))
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

    _strip_scene(bpy)
    cam, sun = _install_camera_and_sun(bpy, viewpoint)
    records = _bake_world_into_meshes(bpy, mathutils)
    fit = _compute_fit(mathutils, records, viewpoint.fit_kind)
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
    ap.add_argument("--viewpoint", required=True, choices=["hex", "square"])
    ap.add_argument("--keep-per-facing", action="store_true",
                    help="write per-facing PNGs alongside the atlas (used by diff)")
    ap.add_argument("--cols-per-row", type=int, default=None)
    return ap.parse_args(argv)


def main(argv):
    import bpy
    import mathutils
    from viewpoints import HEX_VIEWPOINT, SQUARE_VIEWPOINT

    args = _parse_args(argv)
    vp = HEX_VIEWPOINT if args.viewpoint == "hex" else SQUARE_VIEWPOINT
    render_atlas(bpy, mathutils, vp, args.out, args.name,
                 cols_per_row=args.cols_per_row,
                 keep_per_facing=args.keep_per_facing)
    return 0


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(argv))
