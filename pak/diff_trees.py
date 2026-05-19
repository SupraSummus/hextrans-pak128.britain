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

    python3 pak/diff_trees.py <blend_path> <upstream_dat> [--ages 4]

`<upstream_dat>` is the upstream pak dat path (e.g. `trees/oak.dat`);
the image-stem prefix is derived from its `image[…]=` refs and the
diff harness appends `-<season>-<age>_<facing>.png` to land on the
upstream PNGs.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from pak import REPO_ROOT

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
    ap.add_argument("upstream_dat", help="upstream pak dat path, e.g. trees/oak.dat")
    ap.add_argument("--ages", type=int, default=4)
    ap.add_argument("--seasons", type=int, default=1, help="render-side season count; phase 1 = 1 (summer only)")
    ap.add_argument("--out", default=None)
    return ap.parse_args(argv)


def _render(blend_path: Path, out_dir: Path, name: str, ages: int, seasons: int) -> None:
    from pak.bake import run_render
    from pak.viewpoints import tree_square_viewpoint
    run_render(blend=blend_path,
               viewpoint=tree_square_viewpoint(ages=ages, seasons=seasons),
               name=name, out_dir=out_dir)


def _compose(
    ours_dir: Path, up_paths: dict[tuple[int, int], Path],
    name: str, ages: int, seasons: int, out_grid: Path,
) -> list[CellMetric]:
    import numpy as np
    from PIL import Image

    from pak.diff import GridCell, cell_metric, compose_grid

    if seasons != 1:
        # Phase-1 scope is summer only (per module docstring); the
        # multi-season grid layout (stacked 3-row blocks, one per
        # season) isn't wired yet.  Re-introduce when the first
        # `seasons=2` tree ports — at which point `compose_grid`
        # itself probably wants a multi-block mode.
        raise NotImplementedError("multi-season tree grid composition not wired")

    cells: list[GridCell] = []
    metrics: list[CellMetric] = []
    s = 0
    for a in range(ages):
        ours = np.asarray(Image.open(ours_dir / f"{name}_A{a}_S{s}.png").convert("RGBA"))
        up = np.asarray(Image.open(up_paths[(a, s)]).convert("RGBA"))
        m, om, um = cell_metric(ours, up, alpha_threshold=16)
        metrics.append(CellMetric(age=a, season=s, iou=m.iou,
                                  xor_px=m.xor_px, drgb=m.drgb))
        cells.append(GridCell(ours, up, om, um, f"age {a}"))

    compose_grid(cells, out_path=out_grid)
    return metrics


def run(blend: str, upstream_dat: str, *, ages: int, seasons: int,
        out_dir: Path, name: str | None = None) -> list[CellMetric]:
    """Render `blend` through tree_square, diff every (age, season) cell
    against `<stem>-<season>-<age>_S.png` (with `<stem>` derived from
    `upstream_dat`'s `image[…]` refs), return per-cell metrics.

    `name` selects which object in a multi-object upstream dat to read
    image refs from (most tree dats are single-object so it can be left
    unset)."""
    from pak.fetch_blend import fetch as fetch_blend
    from pak.fetch_pak import fetch as fetch_pak
    from pak.upstream import image_stem

    out_dir.mkdir(parents=True, exist_ok=True)
    blend_path = fetch_blend(blend)
    render_name = Path(blend).stem
    _render(blend_path, out_dir, render_name, ages, seasons)

    stem = image_stem(upstream_dat, name=name)
    up_paths: dict[tuple[int, int], Path] = {}
    for s in range(seasons):
        tag = _SEASON_TAGS[s]
        for a in range(ages):
            up_paths[(a, s)] = fetch_pak(f"{stem}-{tag}-{a}_S.png")
    return _compose(out_dir, up_paths, render_name, ages, seasons, out_dir / "grid.png")


def format_table(metrics: list[CellMetric]) -> str:
    lines = [f"{'a':>2} {'s':>2}  {'IoU':>6}  {'XOR_px':>7}  {'dRGB(in)':>9}"]
    for m in metrics:
        lines.append(f"{m.age:>2} {m.season:>2}  {m.iou:>6.3f}  {m.xor_px:>7d}  {m.drgb:>9.2f}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = _parse(argv)
    out_dir = Path(args.out) if args.out else REPO_ROOT / "out" / "diff_trees" / Path(args.upstream_dat).stem
    metrics = run(args.blend, args.upstream_dat, ages=args.ages, seasons=args.seasons, out_dir=out_dir)
    print(f"wrote {out_dir / 'grid.png'}")
    print(format_table(metrics))
    worst = min(m.iou for m in metrics)
    print(f"worst IoU: {worst:.3f}  (<{FAIL_IOU:.2f} fails)")
    return 0 if worst >= FAIL_IOU else 1


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.exit(main(sys.argv[1:]))
