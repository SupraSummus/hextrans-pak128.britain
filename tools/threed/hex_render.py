"""Hex-camera headless renderer for the upstream Pak128.Britain blends.

Sibling to `blend_render.py` (which reproduces the square-dimetric
upstream view).  This one renders into the hex projection defined in
`hextrans/src/simutrans/display/hex_proj.h` (mirrored in `hex_synth.py`).

Strategy: pre-shear the model under a parent Empty so the projection's
anisotropic y/z scales survive Blender's isotropic ortho camera.  The
camera looks straight along world +Y; the parent Empty's matrix encodes
shear and per-facing Z rotation.  Sun is one fixed world-direction; the
model rotates beneath it (pak128 convention -- see CLAUDE.md ->
"Structural anchors").

Output is a single atlas PNG `<name>.png`: one row, cells laid out in
the `_VIEWS` order below.  The .dat references cells as
`<name>.<col>.<row>` (Simutrans image-sheet convention).  Atlas
composition follows `hextrans-pak128/tools/threed/bespoke.py::bake_atlas`
but runs in-Blender via numpy + bpy (Blender ships numpy, not PIL).

Run as:

    blender -b <blend_path> -P tools/threed/hex_render.py -- \\
        --out out/<asset> --name <stem> [--views 8|6|4]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from math import radians
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from hex_synth import (  # noqa: E402
    DEFAULT_W, HEX_TILE_RADIUS, SUN_DIR, hex_proj_shear,
)


# Pakset-wide scale carrying upstream Britain blends into hex world units.
# Upstream blends are authored against a fixed ortho camera with
# `ortho_scale = 24` rendering to 128 px (`blend_render.py` reproduces this
# verbatim).  Hex uses `ortho_scale = 2 * HEX_TILE_RADIUS` at the same image
# width.  The ratio is the single constant that takes any upstream blend's
# native frame into hex world units while preserving relative sizes between
# assets (a long loco stays bigger than a short carriage).
BLEND_ORTHO_SCALE = 24.0
_BLEND_TO_HEX_SCALE = (2.0 * HEX_TILE_RADIUS) / BLEND_ORTHO_SCALE


# (suffix, model Z rotation deg).  Same 8-direction labels as
# blend_render.py so dat files port without facing relabelling.
_VIEWS = [
    ("S",   0),
    ("SW", 45),
    ("W",  90),
    ("NW",135),
    ("N", 180),
    ("NE",225),
    ("E", 270),
    ("SE",315),
]
_FOUR = {"S", "W", "N", "E"}
_SIX = {"S", "SW", "NW", "N", "NE", "SE"}


def _parse_args(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--views", type=int, choices=[4, 6, 8], default=8)
    ap.add_argument("--width", type=int, default=DEFAULT_W,
                    help="output image width (and height) in pixels")
    ap.add_argument("--cols-per-row", type=int, default=None,
                    help="atlas grid width; default lays all cells in one row")
    return ap.parse_args(argv)


def _setup_camera(bpy, mathutils, width: int) -> None:
    """Override the scene's camera into an ortho view aligned for hex.

    Camera position: south of origin, looking north (+Y).  Standard
    Blender 'front view'.  Ortho_scale = 2R so world x in [-R, R] maps
    to the image's full width.
    """
    cam = bpy.data.objects.get("Camera")
    if cam is None:
        raise SystemExit("scene has no object named 'Camera'")
    cam.rotation_mode = "XYZ"
    # World z=0 lands at row `mid_y = top_pad + u = w/2 + u` of a w-tall
    # image; lifting the camera by `(mid_y - h/2) / pixels_per_world` puts
    # the ground row at mid_y and leaves the `top_pad` band of headroom
    # above for z-lifted geometry (vehicles tilted via shear, deck heights).
    # For W=128: mid_y=96, h=128, so lift = (96 - 64) / 64 = 0.5 world units.
    pixels_per_world = width / (2.0 * HEX_TILE_RADIUS)
    mid_y = width // 4 + width // 2  # top_pad (w/2) + u (w/4)
    z_lift = (mid_y - width / 2.0) / pixels_per_world
    cam.location = (0.0, -10.0, z_lift)
    cam.rotation_euler = (radians(90), 0.0, 0.0)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 2.0 * HEX_TILE_RADIUS

    scn = bpy.context.scene
    scn.render.resolution_x = width
    scn.render.resolution_y = width
    scn.render.resolution_percentage = 100
    scn.render.film_transparent = True


def _setup_sun(bpy) -> None:
    """One fixed world sun: from south, 60 deg above horizon.

    Reuses the scene's existing 'Sphere' object (the upstream blends'
    sun).  Lamp's local -Z is the light direction; rotating 30 deg around
    X takes -Z from (0,0,-1) to (0, sin30, -cos30) = (0, 0.5, -sqrt3/2),
    matching `SUN_DIR`.
    """
    sun = bpy.data.objects.get("Sphere")
    if sun is None:
        return  # not all blends carry the named sun; leave default lighting
    sun.rotation_mode = "XYZ"
    sun.rotation_euler = (radians(30), 0.0, 0.0)


def _reparent_to_shear_root(bpy, mathutils) -> tuple["bpy.types.Object", "mathutils.Matrix"]:
    """Create an Empty whose matrix_basis carries the hex projection
    shear, parent every existing world-space object (except the camera
    and the sun) under it.  Per-facing rotation will compose onto this
    Empty's matrix_basis.

    The `fit` 4x4 carries upstream's standardised frame into hex world
    units: a single pakset-wide scale (`_BLEND_TO_HEX_SCALE`), XY centring
    so the asset sits on the tile, and a Z-floor adjustment so the
    lowest visible geometry rests at z=0.  No per-asset rotation: the
    upstream Britain blends are authored with the long axis along world
    Y, and the per-facing `rot_z` in `_VIEWS` handles all turning.

    Returns (root_empty, fit_matrix).
    """
    M = mathutils.Matrix
    V = mathutils.Vector
    scn = bpy.context.scene
    skip = {"Camera", "Sphere"}

    pts = []
    for obj in scn.objects:
        if obj.type != "MESH" or obj.name in skip or obj.hide_render:
            continue
        for v in obj.bound_box:
            pts.append(obj.matrix_world @ V(v))
    if not pts:
        raise SystemExit("no renderable mesh objects to fit")
    xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
    cx = (min(xs) + max(xs)) / 2.0
    cy = (min(ys) + max(ys)) / 2.0
    z_floor = min(zs)

    fit = M.Scale(_BLEND_TO_HEX_SCALE, 4) @ M.Translation((-cx, -cy, -z_floor))

    root = bpy.data.objects.new("hex_proj_root", None)
    scn.collection.objects.link(root)
    for obj in list(scn.objects):
        if obj.name in skip or obj is root:
            continue
        if obj.parent is None:
            obj.parent = root
            obj.matrix_parent_inverse = M.Identity(4)
    return root, fit


def _facing_matrix(mathutils, rot_z_deg: int, fit: "mathutils.Matrix") -> "mathutils.Matrix":
    """`shear @ facing_rotation @ fit` -- root matrix for one facing.

    Order applies right-to-left: model (raw blend coords) -> fit (centered,
    scaled to hex tile) -> facing rotation -> shear (projection).
    """
    M = mathutils.Matrix
    shear = M(hex_proj_shear())
    rot = M.Rotation(radians(rot_z_deg), 4, "Z")
    return shear @ rot @ fit


def _load_rgba(bpy, path: Path):
    """Load a PNG via Blender, return its pixels as a top-down (h, w, 4)
    numpy float32 array in [0, 1].

    Blender stores `image.pixels` bottom-up; flip on load so the
    in-memory convention matches `bespoke.bake_atlas` (PIL, top-down)
    and bbox printouts read row-from-top.
    """
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
    """Echo bbox per cell, mirroring `bespoke.bake_atlas`'s printout."""
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


def main(argv: list[str]) -> int:
    import bpy  # only resolvable inside Blender
    import mathutils
    import numpy as np

    args = _parse_args(argv)
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    _setup_camera(bpy, mathutils, args.width)
    _setup_sun(bpy)
    root, fit = _reparent_to_shear_root(bpy, mathutils)

    tmp_dir = out_dir / ".hex_render_tmp"
    tmp_dir.mkdir(exist_ok=True)
    scn = bpy.context.scene
    cells = []
    try:
        for suffix, rot_z in _VIEWS:
            if args.views == 4 and suffix not in _FOUR:
                continue
            if args.views == 6 and suffix not in _SIX:
                continue
            root.matrix_basis = _facing_matrix(mathutils, rot_z, fit)
            tmp_path = tmp_dir / f"{suffix}.png"
            scn.render.filepath = str(tmp_path)
            bpy.ops.render.render(animation=False, write_still=True)
            cells.append((suffix, _load_rgba(bpy, tmp_path)))

        cols = args.cols_per_row or len(cells)
        rows = (len(cells) + cols - 1) // cols
        h, w = cells[0][1].shape[:2]
        atlas = np.zeros((rows * h, cols * w, 4), dtype=np.float32)
        for i, (_, cell) in enumerate(cells):
            r, c = divmod(i, cols)
            atlas[r * h:(r + 1) * h, c * w:(c + 1) * w] = cell

        out_path = out_dir / f"{args.name}.png"
        _save_atlas(bpy, atlas, args.name, out_path)
        _print_atlas_summary(out_path, cells, cols, rows)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return 0


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(argv))
