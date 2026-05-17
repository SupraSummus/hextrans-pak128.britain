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
        <upstream_png_stem_in_pak_repo> \\
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
imports a bake script and reads `BLEND` + `UPSTREAM_STEM` from the
module, so callers don't carry two paths.  `diff_upstream.run()`
returns structured metrics for programmatic callers.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from pak import REPO_ROOT

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
    ap.add_argument("stem", help="upstream png stem in the pak repo, e.g. trains/carriages/4wheel-1850-first-lnwr")
    ap.add_argument("--views", type=int, choices=[4, 8], default=8)
    ap.add_argument("--out", default=None, help="output dir (default: out/diff/<stem-basename>)")
    return ap.parse_args(argv)


def _render(blend_path: Path, out_dir: Path, name: str) -> None:
    script = HERE / "render.py"
    cmd = [
        "blender", "-b", str(blend_path), "-P", str(script), "--",
        "--out", str(out_dir), "--name", name,
        "--viewpoint", "square", "--keep-per-facing",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def _compose(ours_dir: Path, up_paths: dict[str, Path], name: str, views: list[str], out_grid: Path) -> list[FacingMetric]:
    import numpy as np
    from PIL import Image, ImageDraw

    from pak.diff import checker, drgb_intersection, iou, silhouette_mask, xor_image

    CELL, PAD, LH = 128, 8, 18
    cols, rows = len(views), 3
    W = cols * (CELL + PAD) + PAD
    H = rows * (CELL + PAD) + PAD + LH

    bg = checker(CELL)
    grid = Image.new("RGBA", (W, H), (245, 245, 245, 255))
    draw = ImageDraw.Draw(grid)

    metrics: list[FacingMetric] = []
    for i, v in enumerate(views):
        draw.text((PAD + i * (CELL + PAD) + CELL // 2 - 6, 2), v, fill=(0, 0, 0, 255))
        ours = Image.open(ours_dir / f"{name}_{v}.png").convert("RGBA")
        up = Image.open(up_paths[v]).convert("RGBA")
        x = PAD + i * (CELL + PAD)
        grid.paste(Image.alpha_composite(bg, ours), (x, LH + PAD))
        grid.paste(Image.alpha_composite(bg, up), (x, LH + PAD + CELL + PAD))
        a = np.asarray(ours, dtype=np.int16)
        b = np.asarray(up, dtype=np.int16)

        am = silhouette_mask(a, alpha_threshold=16)
        bm = silhouette_mask(b, alpha_threshold=16)
        xor_px = int((am ^ bm).sum())
        metrics.append(FacingMetric(
            facing=v,
            iou=iou(am, bm),
            xor_px=xor_px,
            drgb=drgb_intersection(a, b, am, bm),
        ))
        grid.paste(Image.fromarray(xor_image(am, bm), "RGBA"),
                   (x, LH + PAD + 2 * (CELL + PAD)))

    out_grid.parent.mkdir(parents=True, exist_ok=True)
    grid.save(out_grid)
    return metrics


def run(blend: str, stem: str, *, views: int = 8, out_dir: Path) -> list[FacingMetric]:
    """Render `blend` through the square viewpoint, diff every facing
    against the matching upstream PNG (`<stem>_<facing>.png`), return
    per-facing metrics.  Side effects: writes `grid.png` and per-facing
    PNGs into `out_dir`.
    """
    from pak.fetch_blend import fetch as fetch_blend
    from pak.fetch_pak import fetch as fetch_pak

    view_list = VIEWS_8 if views == 8 else VIEWS_4
    out_dir.mkdir(parents=True, exist_ok=True)
    blend_path = fetch_blend(blend)
    render_name = Path(blend).stem
    _render(blend_path, out_dir, render_name)
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
    stem_name = Path(args.stem).name
    out_dir = Path(args.out) if args.out else REPO_ROOT / "out" / "diff" / stem_name

    metrics = run(args.blend, args.stem, views=args.views, out_dir=out_dir)

    print(f"wrote {out_dir / 'grid.png'}")
    print(format_table(metrics))
    worst = min(m.iou for m in metrics)
    print(f"worst IoU: {worst:.3f}  (typical calibrated assets >= 0.93; <{FAIL_IOU:.2f} fails)")
    return 0 if worst >= FAIL_IOU else 1


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.exit(main(sys.argv[1:]))
