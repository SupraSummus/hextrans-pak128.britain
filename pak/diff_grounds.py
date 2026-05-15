#!/usr/bin/env python3
"""Pixel-diff a ground baker's square-projection output vs. upstream.

Test harness for the parametric ground synth pipeline.  We re-run a
hex `grounds/<asset>.py` baker through `SquareGeom` and compare its
81-slope atlas against the authored upstream pak128.Britain PNG cell
by cell — exercising slope decode, region partition, Lambert region
shading, polygon fill, edge sealing and the bake/atlas driver in one
pass.  The diff is intentionally noisy on absolute colour scale
(upstream uses pak128-standard's lightmap multiplier convention,
not ours; see `lightmap.py`); the load-bearing signal is **per-cell
silhouette IoU and per-region brightness ratio**, both of which fall
out of the same generation code regardless of palette.

The slope → cell map is parsed live from upstream's
`grounds/TextureGrounds.dat` (fetched via `fetch_pak.py`), so the
harness picks up any upstream slope-keying changes through the
`pak.lock` SHA bump rather than a stale local table.

Usage:
    python3 -m pak.diff_grounds light_texture
    python3 -m pak.diff_grounds light_texture --out out/lt_diff.png

Exits non-zero if any slope drops below the asset's `min_iou` floor
(see `ASSETS` below — each entry's floor is set slightly under the
current measured min, so future generation-code regressions surface
without flagging today's baseline).  `--min-iou` overrides the
per-asset floor when tightening the bar after a quality improvement.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

from pak import REPO_ROOT
from pak.fetch_pak import fetch as fetch_pak


# Outside-silhouette fill upstream uses on the lightmap (engine reads it
# as "no climate-texture multiplier here"); the hex baker writes alpha=0
# at the same locations.  We strip both conventions to a common silhouette
# mask before comparing.
UPSTREAM_OUT_RGB = (231, 255, 255)


# Each baker family declared here once.  `upstream_png` / `upstream_dat`
# are the pak.lock-fetched upstream artefacts; `asset_basename` is the
# baker's output PNG name (matches `asset_name=` in the bake script's
# `bake_pakset` call); `min_iou` is the per-asset regression floor — set
# slightly below the current measured min so future changes that
# DEGRADE the generation fail CI, without flagging today's baseline.
ASSETS: dict[str, dict] = {
    "light_texture": {
        "module": "grounds.light_texture",
        "asset_basename": "light_texture",
        "upstream_png": "grounds/images/texture-lightmap.png",
        "upstream_dat": "grounds/TextureGrounds.dat",
        "upstream_obj": "LightTexture",
        # Current measurement: mean IoU 0.97, min 0.90.  Floor at 0.88
        # leaves a small margin for unrelated rasterisation tweaks.
        "min_iou": 0.88,
    },
}


def parse_slope_to_cell(dat_path: Path,
                        obj_name: str | None = None) -> dict[int, tuple[int, int]]:
    """`{slope_id: (row, col)}` from a ground dat's `Image[N]` entries
    pointing at `<stem>.<row>.<col>`.

    Upstream `landscape/grounds/TextureGrounds.dat` is multi-object —
    LightTexture, ClimateTexture, ShoreTransition all share the
    `Image[0][0]` namespace.  `obj_name` selects which `Name=`
    declaration's entries to keep; when omitted, the first object's
    entries are returned."""
    name_pat = re.compile(r"Name=(\S+)")
    img_pat = re.compile(r"Image\[(\d+)\]\[0\]=\S+\.(\d+)\.(\d+)")
    out: dict[int, tuple[int, int]] = {}
    current_name: str | None = None
    target_name = obj_name
    for line in dat_path.read_text(errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        m = name_pat.match(stripped)
        if m:
            current_name = m.group(1)
            if target_name is None:
                target_name = current_name
            continue
        m = img_pat.match(stripped)
        if m and current_name == target_name:
            out[int(m.group(1))] = (int(m.group(2)), int(m.group(3)))
    return out


def square_bake(module_name: str, asset_basename: str,
                work_dir: Path) -> tuple[np.ndarray, dict[int, tuple[int, int]]]:
    """Square-bake an asset module by exec-ing it with `--projection square`.

    Returns `(atlas, slope_to_cell)` where `slope_to_cell` is parsed
    out of the freshly-emitted `<asset>.dat` so the cell layout matches
    what the baker actually wrote (not a recomputed index, which would
    be wrong if `iter_valid_slopes` skips slopes)."""
    cmd = [sys.executable, "-m", module_name,
           "--projection", "square",
           "--out-dir", str(work_dir)]
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)
    atlas = np.array(Image.open(work_dir / f"{asset_basename}.png").convert("RGBA"))
    slope_to_cell = parse_slope_to_cell(work_dir / f"{asset_basename}.dat")
    return atlas, slope_to_cell


def slice_cell(atlas: np.ndarray, row: int, col: int,
               cell_w: int = 128, cell_h: int = 128) -> np.ndarray:
    return atlas[row * cell_h:(row + 1) * cell_h,
                 col * cell_w:(col + 1) * cell_w]


def silhouette_from_alpha(cell: np.ndarray) -> np.ndarray:
    """Our convention: RGBA, alpha=0 outside the silhouette."""
    return cell[..., 3] > 0


def silhouette_from_cyan(cell: np.ndarray) -> np.ndarray:
    """Upstream convention: RGB matches `UPSTREAM_OUT_RGB` outside."""
    out = np.all(cell[..., :3] == np.array(UPSTREAM_OUT_RGB), axis=-1)
    return ~out


def luminance(cell: np.ndarray) -> np.ndarray:
    """Inside-silhouette grey signal.  Upstream is RGB-tinted but the
    Lambert is carried by the G channel (R drops to ~215 outside the
    silhouette as a climate-routing hint); ours is uniform-grey so any
    channel reads the same."""
    return cell[..., 1].astype(np.float32)


def iou(mask_a: np.ndarray, mask_b: np.ndarray) -> float:
    inter = int(np.logical_and(mask_a, mask_b).sum())
    union = int(np.logical_or(mask_a, mask_b).sum())
    return 1.0 if union == 0 else inter / union


def per_cell_diff(ours: np.ndarray, upstream: np.ndarray) -> dict:
    """Compare one cell — ours (RGBA, alpha-out) vs upstream (RGB, cyan-out)."""
    our_sil = silhouette_from_alpha(ours)
    up_sil = silhouette_from_cyan(upstream)
    sil_iou = iou(our_sil, up_sil)

    # Per-region brightness ratio: walk our distinct grey values, compute
    # the mean of upstream's pixels under the same mask, report ratios.
    inside_both = np.logical_and(our_sil, up_sil)
    if not inside_both.any():
        return {"iou": sil_iou, "our_mean": None, "up_mean": None, "ratio": None}

    our_lum = luminance(ours)[inside_both].mean()
    up_lum = luminance(upstream)[inside_both].mean()
    ratio = up_lum / our_lum if our_lum > 0 else None
    return {"iou": sil_iou, "our_mean": float(our_lum),
            "up_mean": float(up_lum), "ratio": ratio}


def make_grid(ours_cells: list[np.ndarray],
              upstream_cells: list[np.ndarray],
              cell_w: int = 128, cell_h: int = 128) -> np.ndarray:
    """Stacked grid: ours on top row, upstream on bottom, one column per cell."""
    n = len(ours_cells)
    grid = np.zeros((2 * cell_h, n * cell_w, 4), dtype=np.uint8)
    for i, (o, u) in enumerate(zip(ours_cells, upstream_cells)):
        grid[:cell_h, i * cell_w:(i + 1) * cell_w] = o
        if u.shape[-1] == 3:
            u = np.dstack([u, np.full(u.shape[:2], 255, dtype=np.uint8)])
        grid[cell_h:2 * cell_h, i * cell_w:(i + 1) * cell_w] = u
    return grid


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("asset", choices=sorted(ASSETS.keys()))
    p.add_argument("--out", type=Path, default=None,
                   help="write a side-by-side grid PNG of the worst N cells")
    p.add_argument("--worst", type=int, default=12,
                   help="how many worst-IoU cells to include in --out (default 12)")
    p.add_argument("--min-iou", type=float, default=None,
                   help="override the asset's calibrated `min_iou` floor")
    args = p.parse_args(argv)

    spec = ASSETS[args.asset]
    up_png = fetch_pak(spec["upstream_png"])
    up_dat = fetch_pak(spec["upstream_dat"])
    upstream = np.array(Image.open(up_png).convert("RGB"))
    slope_to_cell = parse_slope_to_cell(up_dat, obj_name=spec.get("upstream_obj"))

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        ours, our_slope_to_cell = square_bake(
            spec["module"], spec["asset_basename"], tmp_path)

    cell_w, cell_h = 128, 128
    rows = []
    for slope in sorted(our_slope_to_cell.keys()):
        if slope not in slope_to_cell:
            continue  # upstream skips this slope; nothing to diff against
        our_r, our_c = our_slope_to_cell[slope]
        our_cell = slice_cell(ours, our_r, our_c, cell_w, cell_h)
        up_r, up_c = slope_to_cell[slope]
        up_cell = slice_cell(upstream, up_r, up_c, cell_w, cell_h)
        d = per_cell_diff(our_cell, up_cell)
        rows.append((slope, d, our_cell, up_cell))

    # Print summary.
    print(f"# {args.asset}: {len(rows)} slopes compared")
    print(f"{'slope':>5}  {'iou':>5}  {'ours':>5}  {'upst':>5}  {'ratio':>5}")
    min_iou = 1.0
    for slope, d, _, _ in rows:
        iou_v = d["iou"]
        min_iou = min(min_iou, iou_v)
        om = f"{d['our_mean']:.0f}" if d["our_mean"] is not None else "  -- "
        um = f"{d['up_mean']:.0f}" if d["up_mean"] is not None else "  -- "
        rt = f"{d['ratio']:.2f}" if d["ratio"] is not None else "  -- "
        print(f"{slope:>5}  {iou_v:5.3f}  {om:>5}  {um:>5}  {rt:>5}")

    # Aggregate.
    iou_arr = np.array([d["iou"] for _, d, _, _ in rows])
    print(f"# IoU: min={iou_arr.min():.3f} mean={iou_arr.mean():.3f} "
          f"<0.95: {int((iou_arr < 0.95).sum())}/{len(iou_arr)}")

    if args.out:
        rows_sorted = sorted(rows, key=lambda r: r[1]["iou"])
        worst = rows_sorted[:args.worst]
        slopes_w = [r[0] for r in worst]
        grid = make_grid([r[2] for r in worst], [r[3] for r in worst])
        args.out.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(grid).save(str(args.out))
        print(f"# wrote {args.out} (worst {len(worst)} slopes: {slopes_w})", file=sys.stderr)

    floor = args.min_iou if args.min_iou is not None else spec["min_iou"]
    if min_iou < floor:
        print(f"# FAIL: min IoU {min_iou:.3f} < floor {floor:.3f}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
