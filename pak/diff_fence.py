#!/usr/bin/env python3
"""Pixel-diff `grounds/fence.blend` rendered through the square cardinal
cameras against upstream pak128.Britain's `fence-{3,4,5}.png`.

Three pairings:

  * E facing  ↔ fence-3 (wall0, left back-edge from W corner up to N)
  * S facing  ↔ fence-4 (wall1, right back-edge from N down to E)
  * E ∪ S     ↔ fence-5 (both diagonals composited into the Λ shape)

Drives `pak/render.py --viewpoint fence_square` and reads the per-facing
PNGs back, same shell-out shape as `pak/diff_buildings.py` and
`pak/diff_upstream.py`.

Usage:
    python3 -m pak.diff_fence
    python3 -m pak.diff_fence --out out/fence_diff.png
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

from pak import REPO_ROOT
from pak.fetch_blend import fetch as fetch_blend
from pak.fetch_pak import fetch as fetch_pak

# Each pairing: which facing(s) of our render get composited (via
# silhouette OR for multi-facing entries) and which upstream basename
# they diff against.
PAIRINGS: list[tuple[tuple[str, ...], str]] = [
    (("E",), "fence-3"),
    (("S",), "fence-4"),
    (("E", "S"), "fence-5"),
]

# Calibration floor — set slightly below the measured baseline so future
# blend / render-pipeline drift trips CI without flagging today's IoU.
# Measured: E↔fence-3 0.862, S↔fence-4 0.896, (E|S)↔fence-5 0.844.
MIN_IOU = 0.80

UPSTREAM_OUT_RGB = (231, 255, 255)


def render_fence_blend(out_dir: Path) -> dict[str, np.ndarray]:
    """Run `pak.render` on `grounds/fence.blend` and return per-facing RGBA."""
    blend_path = fetch_blend("grounds/fence.blend")
    script = REPO_ROOT / "pak" / "render.py"
    cmd = ["blender", "-b", str(blend_path), "-P", str(script), "--",
           "--out", str(out_dir), "--name", "fence_blend",
           "--viewpoint", "fence_square", "--keep-per-facing"]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    return {label: np.array(Image.open(out_dir / f"fence_blend_{label}.png"))
            for label in ("S", "W", "N", "E")}


def _silhouette(arr: np.ndarray) -> np.ndarray:
    """Boolean mask from RGBA (alpha>0) or RGB+magic-pink (upstream)."""
    if arr.shape[-1] == 4:
        return arr[..., 3] > 0
    return ~np.all(arr[..., :3] == np.array(UPSTREAM_OUT_RGB), axis=-1)


def _iou(a: np.ndarray, b: np.ndarray) -> float:
    inter = int(np.logical_and(a, b).sum())
    union = int(np.logical_or(a, b).sum())
    return 1.0 if union == 0 else inter / union


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path, default=None,
                   help="write a 2-row grid PNG: ours on top, upstream below")
    p.add_argument("--min-iou", type=float, default=MIN_IOU,
                   help=f"calibration floor (default {MIN_IOU})")
    args = p.parse_args(argv)

    with tempfile.TemporaryDirectory() as tmp:
        ours = render_fence_blend(Path(tmp))

    upstreams = {f"fence-{n}": np.array(Image.open(fetch_pak(
        f"grounds/images/fence-{n}.png"))) for n in (3, 4, 5)}

    print(f"{'pair':>16}  {'iou':>5}")
    min_iou = 1.0
    grid_pairs: list[tuple[np.ndarray, np.ndarray]] = []
    for labels, up_name in PAIRINGS:
        arrs = [ours[l] for l in labels]
        our_sil = np.zeros(arrs[0].shape[:2], dtype=bool)
        our_rgba = np.zeros_like(arrs[0])
        for a in arrs:
            our_sil |= _silhouette(a)
            our_rgba = np.maximum(our_rgba, a)
        up = upstreams[up_name]
        iou_v = _iou(our_sil, _silhouette(up))
        min_iou = min(min_iou, iou_v)
        pair_label = "|".join(labels) + " vs " + up_name
        print(f"  {pair_label:>14}  {iou_v:5.3f}")
        grid_pairs.append((our_rgba, up))

    if args.out:
        W = 128
        grid = np.full((W * 2 + 20, W * len(grid_pairs), 4), 255, dtype=np.uint8)
        for i, (our_rgba, up) in enumerate(grid_pairs):
            grid[:W, i*W:(i+1)*W] = our_rgba
            if up.shape[-1] == 3:
                up = np.dstack([up, np.full(up.shape[:2], 255, dtype=np.uint8)])
            grid[W+20:W*2+20, i*W:(i+1)*W] = up
        args.out.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(grid).save(str(args.out))
        print(f"# wrote {args.out}", file=sys.stderr)

    if min_iou < args.min_iou:
        print(f"# FAIL: min IoU {min_iou:.3f} < floor {args.min_iou:.3f}",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
