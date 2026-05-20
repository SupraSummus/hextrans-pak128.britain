"""Calibration check for bridge spans against the upstream pak atlas.

Bridges in upstream Britain ship as a single multi-row atlas
(`images/<bridge>.png`) addressed by `<file>.<row>.<col>` rather than
the per-facing PNGs vehicles use.  Each cardinal facing of the bridge
silhouette is the alpha-composite of two cells: `BackImage[<axis>][0]`
underneath, `FrontImage[<axis>][0]` on top (the depth-clip layers the
engine paints on either side of the train sprite).

Today the harness only diffs the "middle" of a straight span (the
`Image[NS]` / `Image[EW]` cells) — the geometry the JH `straight.blend`
actually models.  Start segments, ramps and pillars come from separate
JH blends and need their own cell-mapping rows; deferred until a full
bridge port lands.

Cell convention from the dat (`ways/plate-girder.dat`):
  - row 0: Back* (start[N,E,S,W], image[EW,NS], ramp[N,W,S,E])
  - row 1: Front* same column order
  - rows 2/3: Back/Front for the second pillar variant `[1]`

Output mirrors `pak.diff_upstream.run()`: per-facing FacingMetric +
`grid.png` (ours / upstream / silhouette XOR).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

CELL = 128

# Upstream `images/<bridge>.png` column convention.  Same column order in
# every row across all rail-bridge dats inspected (`beam-bridge.dat`,
# `plate-girder.dat`).  Mapped to dat-facing labels per column so the
# diff tooling can name cells the way the dat reads them.
START_COLS = {"N": 0, "E": 1, "S": 2, "W": 3}
IMAGE_COLS = {"EW": 4, "NS": 5}
RAMP_COLS = {"N": 6, "W": 7, "S": 8, "E": 9}

# Compass-facing render labels in canonical bridge_square_viewpoint
# order — bridge_square renders S, W, N, E (the order in
# `_UPSTREAM_NORMAL_CARDINAL`).
RENDER_FACINGS = ("S", "W", "N", "E")


@dataclass(frozen=True)
class FacingMetric:
    facing: str
    iou: float
    xor_px: int
    drgb: float


def _composite_cell(atlas, row_back: int, row_front: int, col: int):
    """Return RGBA `Image` of the `(row_back, col)` cell with the
    `(row_front, col)` cell alpha-composited on top — the engine's
    back/front draw order for one bridge facing.
    """
    from PIL import Image

    from pak.diff import key_magic_pink_to_alpha

    x = col * CELL
    back = key_magic_pink_to_alpha(
        atlas.crop((x, row_back * CELL, x + CELL, row_back * CELL + CELL))
    )
    front = key_magic_pink_to_alpha(
        atlas.crop((x, row_front * CELL, x + CELL, row_front * CELL + CELL))
    )
    out = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    out.alpha_composite(back)
    out.alpha_composite(front)
    return out


def run(
    *,
    rendered_dir: Path,
    render_stem: str,
    atlas_path: Path,
    asset: str = "image",
    variant: int = 0,
    out_dir: Path,
) -> list[FacingMetric]:
    """Diff the rendered S/W/N/E facings against the upstream atlas
    cells for the named `asset` and pillar variant (0 or 1).

    `asset` selects which atlas column group + facing→cell mapping
    to use: `image` (middle of a straight span, 2 axis-labelled cells
    shared across pairs of facings), `start` (4 direction-labelled
    end cells), `ramp` (4 direction-labelled slope cells).  The
    facing→cell mapping for each asset was discovered by running
    `match` mode (the per-facing IoU against every column in the
    group) for one plate-girder blend and reading off the maximum.

    Side effects: writes `grid.png` and per-cell upstream PNGs (debug)
    into `out_dir`.
    """
    atlas, row_back, row_front = _open_atlas(atlas_path, variant)
    cells_per_facing = _cells_for_asset(asset, atlas, row_back, row_front)
    return _grid_and_metrics(
        rendered_dir, render_stem, cells_per_facing, out_dir,
    )


def _open_atlas(atlas_path: Path, variant: int):
    from PIL import Image
    atlas = Image.open(atlas_path).convert("RGBA")
    row_back = 0 if variant == 0 else 2
    return atlas, row_back, row_back + 1


def _cells_for_asset(asset: str, atlas, row_back: int, row_front: int) -> dict:
    """Return `{render_facing: upstream_cell_image}` per the discovered
    facing→cell mapping for `asset`.

    Bridge orientation vs. camera facing in JH's plate-girder blends:
    each blend's geometry runs along world +X and the four
    normal-alignment cameras shoot from the four map corners.  Under
    the S camera (at +X, -Y, dimetric NW look) the bridge appears
    running NE-SW on screen — i.e. the **EW** map axis; the N camera
    mirrors that.  The E/W cameras shoot the bridge end-on,
    producing the **NS** map axis on screen.  Start and Ramp cells
    follow the same on-screen-axis logic with direction labels: the
    S-camera EW-axis view matches both `Start[E]` and `Start[W]`
    depending on which end the blend models (BackStart[E] for an
    east-facing bridge end, BackStart[W] for west).  The mapping
    below was discovered empirically by running `match` mode against
    `end.blend` / `slope.blend` and picking the row maxima."""
    if asset == "image":
        # 2 axis cells shared across pairs of facings
        return {
            "S": _composite_cell(atlas, row_back, row_front, IMAGE_COLS["EW"]),
            "N": _composite_cell(atlas, row_back, row_front, IMAGE_COLS["EW"]),
            "E": _composite_cell(atlas, row_back, row_front, IMAGE_COLS["NS"]),
            "W": _composite_cell(atlas, row_back, row_front, IMAGE_COLS["NS"]),
        }
    if asset == "start":
        return _start_or_ramp_cells(atlas, row_back, row_front, START_COLS)
    if asset == "ramp":
        return _start_or_ramp_cells(atlas, row_back, row_front, RAMP_COLS)
    raise SystemExit(f"unknown asset: {asset!r} (image|start|ramp)")


def _start_or_ramp_cells(atlas, row_back, row_front, cols: dict[str, int]) -> dict:
    # Render-facing → cell label is a uniform 90° CCW shift across the
    # plate-girder family: S camera renders the BackStart/BackRamp[E]
    # cell, W → [S], N → [W], E → [N].  Discovered via `match` mode on
    # `end.blend` (best IoU 0.54-0.59 per facing on its anti-diagonal)
    # and confirmed on `slope.blend` (0.52-0.65).  Same rotation that
    # the `image` mapping above encodes coarsely (S/N→EW, E/W→NS); the
    # finer four-direction asset classes need the per-direction form.
    facing_to_label = {"S": "E", "W": "S", "N": "W", "E": "N"}
    return {
        facing: _composite_cell(atlas, row_back, row_front, cols[label])
        for facing, label in facing_to_label.items()
    }


def _grid_and_metrics(rendered_dir, render_stem, upstream_cells, out_dir):
    import numpy as np
    from PIL import Image

    from pak.diff import MAGIC_PINK, GridCell, cell_metric, compose_grid

    out_dir.mkdir(parents=True, exist_ok=True)
    for facing, im in upstream_cells.items():
        im.save(out_dir / f"upstream_{facing}.png")

    cells: list[GridCell] = []
    metrics: list[FacingMetric] = []
    for v, up_img in upstream_cells.items():
        ours = np.asarray(Image.open(rendered_dir / f"{render_stem}_{v}.png")
                          .convert("RGBA"))
        up = np.asarray(up_img)
        # `alpha_threshold=0`: upstream bridge cells are tightly
        # anti-aliased; dropping AA edges at `>16` would inflate XOR
        # drift on the silhouette ring.
        m, om, um = cell_metric(ours, up, alpha_threshold=0,
                                magic_rgb=MAGIC_PINK)
        metrics.append(FacingMetric(facing=v, iou=m.iou,
                                    xor_px=m.xor_px, drgb=m.drgb))
        cells.append(GridCell(ours, up, om, um, v))
    compose_grid(cells, out_path=out_dir / "grid.png",
                 strip_magic_rgb=MAGIC_PINK)
    return metrics


def match(
    *,
    rendered_dir: Path,
    render_stem: str,
    atlas_path: Path,
    cols: dict[str, int],
    variant: int = 0,
) -> dict[str, dict[str, float]]:
    """Score every (render_facing, upstream_column) pair's silhouette
    IoU.  Returns `{render_facing: {col_label: iou}}` so the caller
    can read off each render facing's best matching column.

    Used to discover the facing→cell mapping for a new bridge blend
    one-time, then locked into `_cells_for_asset`.  `cols` is the
    `{label: column_index}` map for the asset class
    (`START_COLS` / `RAMP_COLS` / `IMAGE_COLS`); each column's
    Back+Front composite is the candidate cell.
    """
    import numpy as np
    from PIL import Image

    from pak.diff import MAGIC_PINK, iou, silhouette_mask

    atlas, row_back, row_front = _open_atlas(atlas_path, variant)
    candidates = {
        label: _composite_cell(atlas, row_back, row_front, col)
        for label, col in cols.items()
    }
    cand_masks = {
        label: silhouette_mask(np.asarray(im, dtype=np.int16),
                               alpha_threshold=0, magic_rgb=MAGIC_PINK)
        for label, im in candidates.items()
    }
    out: dict[str, dict[str, float]] = {}
    for facing in RENDER_FACINGS:
        ours = Image.open(rendered_dir / f"{render_stem}_{facing}.png").convert("RGBA")
        am = silhouette_mask(np.asarray(ours, dtype=np.int16),
                             alpha_threshold=0, magic_rgb=MAGIC_PINK)
        out[facing] = {label: iou(am, bm) for label, bm in cand_masks.items()}
    return out


def format_match(scores: dict[str, dict[str, float]]) -> str:
    labels = list(next(iter(scores.values())).keys())
    lines = ["       " + "  ".join(f"{lbl:>6}" for lbl in labels)
             + "    best"]
    for facing, row in scores.items():
        best = max(row, key=row.get)
        cells = "  ".join(f"{row[lbl]:6.3f}" for lbl in labels)
        lines.append(f"  {facing}  {cells}    {best} ({row[best]:.3f})")
    return "\n".join(lines)


def format_table(metrics: list[FacingMetric]) -> str:
    lines = [f"{'view':>4}  {'IoU':>6}  {'XOR_px':>7}  {'dRGB':>7}"]
    for m in metrics:
        lines.append(f"{m.facing:>4}  {m.iou:>6.3f}  {m.xor_px:>7d}  {m.drgb:>7.2f}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    import argparse

    from pak import REPO_ROOT
    from pak.fetch_pak import fetch as fetch_pak

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("rendered_dir", help="dir holding <stem>_<facing>.png")
    ap.add_argument("stem", help="rendered atlas stem, e.g. straight")
    ap.add_argument("upstream_atlas",
                    help="path in upstream pak repo, e.g. ways/images/plate-girder.png")
    ap.add_argument("--asset", default="image",
                    choices=["image", "start", "ramp"],
                    help="cell group to diff against (image|start|ramp)")
    ap.add_argument("--match", action="store_true",
                    help="print the full per-facing IoU matrix against "
                         "every column in the asset group, used to "
                         "discover a new blend's facing→cell mapping; "
                         "skips grid/metrics output")
    ap.add_argument("--variant", type=int, default=0, choices=[0, 1],
                    help="pillar variant: 0 = `BackImage`/`Start`/`Ramp` dat "
                         "keys (rows 0/1 of the atlas, gentler abutment "
                         "slope); 1 = `BackImage2`/`Start2`/`Ramp2` keys "
                         "(rows 2/3, steeper abutment slope).  Distinct "
                         "from the trailing `[0]/[1]` season index in the "
                         "dat (`[0]` = summer atlas, `[1]` = a separate "
                         "`-snow.png` atlas) which the diff doesn't model")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    atlas = fetch_pak(args.upstream_atlas)
    if args.match:
        cols = {"image": IMAGE_COLS, "start": START_COLS, "ramp": RAMP_COLS}[args.asset]
        scores = match(
            rendered_dir=Path(args.rendered_dir),
            render_stem=args.stem,
            atlas_path=atlas,
            cols=cols,
            variant=args.variant,
        )
        print(format_match(scores))
        return 0
    out_dir = (Path(args.out) if args.out
               else REPO_ROOT / "out" / "diff" /
               f"{Path(args.upstream_atlas).stem}-{args.stem}-{args.asset}")
    metrics = run(
        rendered_dir=Path(args.rendered_dir),
        render_stem=args.stem,
        atlas_path=atlas,
        asset=args.asset,
        variant=args.variant,
        out_dir=out_dir,
    )
    print(f"wrote {out_dir / 'grid.png'}")
    print(format_table(metrics))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
