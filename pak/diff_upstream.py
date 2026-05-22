"""Calibration check: render an upstream blend through `render.py`
with the square viewpoint and pixel-diff each facing against the
upstream pakset PNG.

Validates the unified renderer's square-dimetric path against the
upstream calibration contract (CLAUDE.md -> "Upstream blend
calibration contract").  Because hex shares the same render path and
the same blend, a passing score here is a necessary precondition for
the hex bake to be right -- it's not sufficient (a procedural hex
reference is still needed; see TODO.md).

Run as:

    python3 pak/diff_upstream.py \\
        <blend_path_in_blends_repo> \\
        <upstream_dat_path_in_pak_repo> \\
        [--views 8|4] [--out out/diff/<name>]

Outputs `<out>/grid.png` (ours / upstream / silhouette-XOR, 8 cols)
and reports two independent per-facing metrics:

  * **Contour** -- silhouette IoU plus symmetric-difference pixel
    count (purely geometry; ignores RGB).
  * **Colour** -- mean abs(RGB-delta) restricted to the silhouette
    intersection (purely colour; ignores geometry mismatches that
    would otherwise inflate the score from missing pixels).

A calibrated asset's bboxes match upstream within +-1 px on every
facing.  Calibrated assets *typically* land at IoU >= 0.93; the
script exits non-zero when any facing falls below 0.90.  A
calibrated asset that fails the bar usually has a material-handling
discrepancy (alpha-blend transparency rendering different in Cycles
vs. upstream's older pipeline) -- check bbox extents to disambiguate
that from real geometry drift.  High colour delta with healthy IoU
traces to upstream's livery material swap (see `TODO.md` -> `sp_*`
mask pass).

Dependencies (system Python, not Blender's bundled): `numpy`, `Pillow`.
Blender (`apt-get install blender`) for the render half.

`pak/check.py` is the more ergonomic entry point -- it
imports a bake script and reads `blend` + `upstream_dat` from the
SPEC, so callers don't carry two paths.  `diff_upstream.run()`
returns structured metrics for programmatic callers.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

from pak import REPO_ROOT
from pak.bake import run_render
from pak.diff import GridCell, cell_metric, compose_grid
from pak.fetch_blend import fetch as fetch_blend
from pak.fetch_pak import fetch as fetch_pak
from pak.upstream import image_stem
from pak.viewpoints import SQUARE_VIEWPOINT

HERE = Path(__file__).resolve().parent
VIEWS_8 = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
VIEWS_4 = ["S", "W", "N", "E"]

# Exit-code threshold.  See module docstring for the IoU mental model.
FAIL_IOU = 0.90


@dataclass(frozen=True)
class FacingMetric:
    facing: str
    iou: float          # silhouette intersection / union; 1.0 == identical contour
    xor_px: int         # |only_ours| + |only_up|; absolute contour-drift magnitude
    drgb: float         # mean abs(RGB-delta) over the silhouette intersection (NaN if empty)


def _parse(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("blend", help="path within the blends repo, e.g. trains/Carriages/4wheel-1850.blend")
    ap.add_argument("upstream_dat", help="upstream dat path in the pak repo, e.g. trains/4wheel-1850s-first.dat")
    ap.add_argument("--views", type=int, choices=[4, 8], default=8)
    ap.add_argument("--out", default=None, help="output dir (default: out/diff/<dat-basename>)")
    return ap.parse_args(argv)


def _render(blend_path: Path, out_dir: Path, name: str) -> None:
    run_render(blend=blend_path, viewpoint=SQUARE_VIEWPOINT,
               name=name, out_dir=out_dir)


def _compose(ours_dir: Path, up_paths: dict[str, Path], name: str, views: list[str], out_grid: Path) -> list[FacingMetric]:
    cells: list[GridCell] = []
    metrics: list[FacingMetric] = []
    for v in views:
        ours = np.asarray(Image.open(ours_dir / f"{name}_{v}.png").convert("RGBA"))
        up = np.asarray(Image.open(up_paths[v]).convert("RGBA"))
        m, om, um = cell_metric(ours, up, alpha_threshold=16)
        metrics.append(FacingMetric(facing=v, iou=m.iou, xor_px=m.xor_px, drgb=m.drgb))
        cells.append(GridCell(ours, up, om, um, v))

    compose_grid(cells, out_path=out_grid)
    return metrics


def run(blend: str, upstream_dat: str, *, views: int = 8, out_dir: Path,
        name: str | None = None) -> list[FacingMetric]:
    """Render `blend` through the square viewpoint, diff every facing
    against the matching upstream PNG (`<stem>_<facing>.png`, with
    `<stem>` derived from `upstream_dat`'s `EmptyImage[…]` refs),
    return per-facing metrics.  Side effects: writes `grid.png` and
    per-facing PNGs into `out_dir`.

    `name` selects which object in a multi-object upstream dat to read
    image refs from (e.g. when a carriage family dat packs five
    vehicles); single-object dats can leave it unset.
    """
    view_list = VIEWS_8 if views == 8 else VIEWS_4
    out_dir.mkdir(parents=True, exist_ok=True)
    blend_path = fetch_blend(blend)
    render_name = Path(blend).stem
    _render(blend_path, out_dir, render_name)
    stem = image_stem(upstream_dat, name=name)
    up_paths = {v: fetch_pak(f"{stem}_{v}.png") for v in view_list}
    return _compose(out_dir, up_paths, render_name, view_list, out_dir / "grid.png")


def format_table(metrics: list[FacingMetric]) -> str:
    """Render metrics as the human-readable table `main()` prints."""
    lines = [f"{'view':>4}  {'IoU':>6}  {'XOR_px':>7}  {'dRGB(in)':>9}"]
    for m in metrics:
        lines.append(f"{m.facing:>4}  {m.iou:>6.3f}  {m.xor_px:>7d}  {m.drgb:>9.2f}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = _parse(argv)
    dat_name = Path(args.upstream_dat).stem
    out_dir = Path(args.out) if args.out else REPO_ROOT / "out" / "diff" / dat_name

    metrics = run(args.blend, args.upstream_dat, views=args.views, out_dir=out_dir)

    print(f"wrote {out_dir / 'grid.png'}")
    print(format_table(metrics))
    worst = min(m.iou for m in metrics)
    print(f"worst IoU: {worst:.3f}  (typical calibrated assets >= 0.93; <{FAIL_IOU:.2f} fails)")
    return 0 if worst >= FAIL_IOU else 1


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.exit(main(sys.argv[1:]))
