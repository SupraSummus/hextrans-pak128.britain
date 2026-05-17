"""Calibration check: render a tree blend through `render.py` with the
square viewpoint and pixel-diff each (age, season) cell against the
upstream pakset PNG.

Mirrors `diff_upstream.py`'s contour + colour metrics for trees.
Cells are addressed as `(age, season)` pairs in `iter_tree_cells`
order (season-major); each maps to an upstream `<stem>-<season>-<age>
_S.png` reference (e.g. `oak-summer-0_S.png`, `oak-autumn-3_S.png`).

Phase-1 scope: summer only (season 0).  Once the per-season leaf-
colour overrides are calibrated, extend `_SEASON_TAGS` to walk the
full 5-row atlas.

Run as:

    python3 pak/diff_trees.py <blend_path> <upstream_stem> [--ages 4]

`<upstream_stem>` is the prefix before the season/age suffix --
`trees/oak` resolves to `trees/oak-summer-0_S.png` and friends.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from pak import REPO_ROOT

HERE = Path(__file__).resolve().parent

# Upstream filename tags per season slot, indexed by the engine's
# season number (0=summer ... 4=winter-snow).  Trees with `seasons=2`
# use ("", "snow") naming -- e.g. `norway-spruce-0_S.png` /
# `norway-spruce-snow-0_S.png` -- and are deferred until the first
# seasons=2 tree ports.
_SEASON_TAGS: tuple[str, ...] = ("summer", "autumn", "winter", "spring", "winter-snow")

FAIL_IOU = 0.85


@dataclass(frozen=True)
class CellMetric:
    age: int
    season: int
    iou: float
    xor_px: int
    drgb: float


def _parse(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("blend", help="path within the blends repo, e.g. trees/oak.blend")
    ap.add_argument("stem", help="upstream filename stem, e.g. trees/oak (matches <stem>-<season>-<age>_S.png)")
    ap.add_argument("--ages", type=int, default=4)
    ap.add_argument("--seasons", type=int, default=1, help="render-side season count; phase 1 = 1 (summer only)")
    ap.add_argument("--out", default=None)
    return ap.parse_args(argv)


def _render(blend_path: Path, out_dir: Path, name: str, ages: int, seasons: int) -> None:
    script = HERE / "render.py"
    cmd = [
        "blender", "-b", str(blend_path), "-P", str(script), "--",
        "--out", str(out_dir), "--name", name,
        "--viewpoint", "tree_square", "--keep-per-facing",
        "--tree-grid", f"{ages},{seasons}",
        "--cols-per-row", str(ages),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def _compose(
    ours_dir: Path, up_paths: dict[tuple[int, int], Path],
    name: str, ages: int, seasons: int, out_grid: Path,
) -> list[CellMetric]:
    import numpy as np
    from PIL import Image, ImageDraw

    from pak.diff import checker, drgb_intersection, iou, silhouette_mask, xor_image

    CELL, PAD, LH = 128, 8, 18
    cols, rows = ages, seasons * 3  # ours / upstream / XOR per season
    W = cols * (CELL + PAD) + PAD
    H = rows * (CELL + PAD) + PAD + LH

    bg = checker(CELL)
    grid = Image.new("RGBA", (W, H), (245, 245, 245, 255))
    draw = ImageDraw.Draw(grid)
    for a in range(ages):
        draw.text((PAD + a * (CELL + PAD) + CELL // 2 - 18, 2),
                  f"age {a}", fill=(0, 0, 0, 255))

    metrics: list[CellMetric] = []
    for s in range(seasons):
        for a in range(ages):
            ours = Image.open(ours_dir / f"{name}_A{a}_S{s}.png").convert("RGBA")
            up = Image.open(up_paths[(a, s)]).convert("RGBA")
            col_x = PAD + a * (CELL + PAD)
            row_y0 = LH + PAD + s * 3 * (CELL + PAD)
            grid.paste(Image.alpha_composite(bg, ours), (col_x, row_y0))
            grid.paste(Image.alpha_composite(bg, up), (col_x, row_y0 + CELL + PAD))

            a_arr = np.asarray(ours, dtype=np.int16)
            b_arr = np.asarray(up, dtype=np.int16)
            am = silhouette_mask(a_arr, alpha_threshold=16)
            bm = silhouette_mask(b_arr, alpha_threshold=16)
            metrics.append(CellMetric(
                age=a, season=s,
                iou=iou(am, bm),
                xor_px=int((am ^ bm).sum()),
                drgb=drgb_intersection(a_arr, b_arr, am, bm),
            ))
            grid.paste(Image.fromarray(xor_image(am, bm), "RGBA"),
                       (col_x, row_y0 + 2 * (CELL + PAD)))

    out_grid.parent.mkdir(parents=True, exist_ok=True)
    grid.save(out_grid)
    return metrics


def run(blend: str, stem: str, *, ages: int, seasons: int, out_dir: Path) -> list[CellMetric]:
    """Render `blend` through tree_square, diff every (age, season) cell
    against `<stem>-<season>-<age>_S.png`, return per-cell metrics."""
    from pak.fetch_blend import fetch as fetch_blend
    from pak.fetch_pak import fetch as fetch_pak

    out_dir.mkdir(parents=True, exist_ok=True)
    blend_path = fetch_blend(blend)
    name = Path(blend).stem
    _render(blend_path, out_dir, name, ages, seasons)

    up_paths: dict[tuple[int, int], Path] = {}
    for s in range(seasons):
        tag = _SEASON_TAGS[s]
        for a in range(ages):
            up_paths[(a, s)] = fetch_pak(f"{stem}-{tag}-{a}_S.png")
    return _compose(out_dir, up_paths, name, ages, seasons, out_dir / "grid.png")


def format_table(metrics: list[CellMetric]) -> str:
    lines = [f"{'a':>2} {'s':>2}  {'IoU':>6}  {'XOR_px':>7}  {'dRGB(in)':>9}"]
    for m in metrics:
        lines.append(f"{m.age:>2} {m.season:>2}  {m.iou:>6.3f}  {m.xor_px:>7d}  {m.drgb:>9.2f}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = _parse(argv)
    out_dir = Path(args.out) if args.out else REPO_ROOT / "out" / "diff_trees" / Path(args.stem).name
    metrics = run(args.blend, args.stem, ages=args.ages, seasons=args.seasons, out_dir=out_dir)
    print(f"wrote {out_dir / 'grid.png'}")
    print(format_table(metrics))
    worst = min(m.iou for m in metrics)
    print(f"worst IoU: {worst:.3f}  (<{FAIL_IOU:.2f} fails)")
    return 0 if worst >= FAIL_IOU else 1


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.exit(main(sys.argv[1:]))
