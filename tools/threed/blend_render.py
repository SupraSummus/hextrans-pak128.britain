"""Square-dimetric headless renderer for the upstream Pak128.Britain blends.

Reproduces the 4/8-view camera + sun positions from
`render_SimutransRender_pak128Britain-65.py` at the repo root, but as a
plain `blender -b -P` script with no addon registration. This is the
square-dimetric output the upstream `.blend`s were authored for; the hex
camera will land separately.

Run as:

    blender -b <blend_path> -P tools/threed/blend_render.py -- \\
        --out out/<asset> --name <stem> [--align bases|vehicles] [--views 8|4]

The scene's existing Camera and Sphere (sun) objects are reused; no
materials are touched (`sp_*` mask pass is not invoked).
"""

from __future__ import annotations

import argparse
import sys
from math import radians


# (suffix, cam rotation Z deg, cam location "bases", cam location "vehicles", sun rotation Z deg)
#
# Copied verbatim from render_SimutransRender_pak128Britain-65.py:
# SCENE_OT_simurender_render_views.execute(). "bases" == op_list "1"
# (default), "vehicles" == op_list "2". All cameras share rotation
# (X=60, Y=0); sun shares (X=90, Y=0).
_VIEWS = [
    ("S",   45,  [10,     -10,    11.6], [ 6.6,   -7.9,   11.6],  90),
    ("SW",  90,  [14.14,   0,     11.6], [ 7.5,    0.6,   10  ], 135),
    ("W",  135,  [10,      10,    11.6], [ 6.72,   8.2,   11.6], 180),
    ("NW", 180,  [ 0,      14.14, 11.6], [ 0,     14.14,  11.6], 225),
    ("N",  225,  [-10,     10,    11.6], [-7,      8.5,   11.6], 270),
    ("NE", 270,  [-14.14,  0,     11.6], [-10.3,  -0.75,  11.6], 315),
    ("E",  315,  [-10,    -10,    11.6], [-32.6, -33.6,   32.5],   0),
    ("SE", 360,  [ 0,     -14.14, 11.6], [ 0,    -11,     11.6],  45),
]
# 4-view subset (op_list "0"): S, W, N, E. Order matches upstream.
_FOUR = {"S", "W", "N", "E"}


def _parse_args(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--name", required=True, help="filename stem; outputs are <name>_<dir>.png")
    ap.add_argument("--align", choices=["bases", "vehicles"], default="bases")
    ap.add_argument("--views", type=int, choices=[4, 8], default=8)
    return ap.parse_args(argv)


def main(argv: list[str]) -> int:
    import bpy  # only resolvable inside Blender

    args = _parse_args(argv)

    scn = bpy.context.scene
    cam = bpy.data.objects.get("Camera")
    sun = bpy.data.objects.get("Sphere")
    if cam is None:
        raise SystemExit("scene has no object named 'Camera'")
    if sun is None:
        raise SystemExit("scene has no object named 'Sphere' (the upstream sun)")
    cam.rotation_mode = "XYZ"
    sun.rotation_mode = "XYZ"

    from pathlib import Path
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for suffix, cam_z, loc_b, loc_v, sun_z in _VIEWS:
        if args.views == 4 and suffix not in _FOUR:
            continue
        cam.rotation_euler = (radians(60), 0.0, radians(cam_z))
        cam.location = loc_v if args.align == "vehicles" else loc_b
        sun.rotation_euler = (radians(90), 0.0, radians(sun_z))
        scn.render.filepath = str(out_dir / f"{args.name}_{suffix}.png")
        bpy.ops.render.render(animation=False, write_still=True)

    return 0


if __name__ == "__main__":
    # Blender passes script args after `--`.
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(argv))
