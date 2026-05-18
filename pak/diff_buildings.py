"""Building diff: two paths sharing the silhouette / dRGB primitives.

`run` is the calibration path — renders a single-tile building blend
through the square viewpoint and pixel-diffs each layout against the
upstream pakset atlas.  Mirrors `diff_upstream.py` for buildings, with
two differences from the vehicle harness:

1. **Layout permutation discovery.**  The dat-level mapping of "layout L
   -> atlas column C" is per-asset (upstream's `BackImage[L][0][0][0][0]
   [0]=...0.C` can permute L vs C freely).  Rather than read both dats
   and stitch them together, this driver computes the full N_layouts x
   N_layouts IoU matrix and prints the best-permutation summary, so the
   matrix itself shows when our hex bake's layout-rotation convention
   matches upstream's vs when it permutes.

2. **Magic-pink transparency.**  Upstream building PNGs are RGB with
   `(231, 255, 255)` as the transparency key (no alpha channel saved);
   our renderer writes proper RGBA.  Silhouette masks normalise across
   both via `_silhouette_mask`.

`run_multitile` is the multi-tile path — reads upstream's dat to
enumerate `(l, y, x, h, phase, season)` cells, slices both the
committed hex atlas (our bake's output) and the upstream square atlas
per their dat refs, and composes a per-cell side-by-side grid.  No
rendering: it's a regression check on what we ship, not a calibration
of what we'd re-bake.  Per-cell IoU is cross-projection (hex vs
square) so it sits in the report as a relative ranking, not a
FAIL_IOU gate — see TODO.md → "Closed (not pursued)" for why
absolute calibration against the shipped multi-tile atlas isn't a
reachable target.

Run via the more ergonomic `pak/check.py` driver (which reads `BLEND`
and `UPSTREAM_STEM` from the bake script), or directly:

    python3 -m pak.diff_buildings \\
        <blend_path_in_blends_repo> \\
        <upstream_png_in_pak_repo> \\
        --layouts 4 [--out out/diff/<name>]
"""

from __future__ import annotations

import argparse
import itertools
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from pak import REPO_ROOT
from pak.diff import MAGIC_PINK, drgb_intersection, iou, silhouette_mask

HERE = Path(__file__).resolve().parent
# Worst-of-best across `res_1600_kg_01`'s four layouts measures 0.905;
# the residual is a Cycles-vs-Blender-internal renderer interior shading
# difference that won't move without a renderer swap (see git log for
# the investigation).  Floor at 0.88 gives a ~0.025-IoU margin matching
# `diff_upstream.FAIL_IOU = 0.90`'s relation to the 0.93 vehicle band.
FAIL_IOU = 0.88


def _silhouette_mask(rgba):
    """Buildings calibrate at `alpha_threshold=0` (not the historical
    16 used by vehicles): EEVEE soft-AA edges otherwise lose ~6% of
    the silhouette and drag IoU from 0.94 to 0.92 even though bboxes
    match upstream within +-1 px.  Upstream building PNGs key
    transparency by `MAGIC_PINK` rather than alpha, so we pass that
    too -- our renders carry alpha and won't match the key colour."""
    return silhouette_mask(rgba, alpha_threshold=0, magic_rgb=MAGIC_PINK)


def _render(blend_path: Path, out_dir: Path, name: str, layouts: int,
            materials: dict | None = None, lighting=None) -> None:
    script = HERE / "render.py"
    cmd = [
        "blender", "-b", str(blend_path), "-P", str(script), "--",
        "--out", str(out_dir), "--name", name,
        "--viewpoint", "square_building",
        "--building-footprint", f"1,1,{layouts},1",
        "--keep-per-facing",
    ]
    if materials:
        import json

        from pak.materials import to_jsonable
        cmd += ["--materials", json.dumps(to_jsonable(materials))]
    if lighting is not None:
        import json
        cmd += ["--lighting", json.dumps(lighting.to_jsonable())]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def _split_upstream(up_png: Path, layouts: int, season_row: int = 0):
    """Slice the upstream atlas into N_layouts 128x128 cells from row
    `season_row` (0=summer, 1=winter).  Returns a list of (h, w, 4)
    numpy arrays in column order."""
    import numpy as np
    from PIL import Image

    full = np.asarray(Image.open(up_png).convert("RGBA"))
    H, W = full.shape[:2]
    if W < 128 * layouts:
        raise SystemExit(
            f"upstream atlas {up_png} is {W}x{H}; needs at least "
            f"{128 * layouts}x128 for {layouts} layouts"
        )
    y0 = season_row * 128
    if H < y0 + 128:
        raise SystemExit(
            f"upstream atlas {up_png} is {W}x{H}; needs at least "
            f"{y0 + 128} rows for season {season_row}"
        )
    return [full[y0:y0 + 128, c * 128:(c + 1) * 128] for c in range(layouts)]


def _parse_backimage_entries(dat_path: Path):
    """Parse a building dat's `backimage[L][y][x][h][p][s]=<basename>.<row>.<col>`
    entries.  Returns list of dicts with keys
    `l, y, x, h, phase, season, row, col`.  Ignores image refs that
    can't be parsed (e.g. `backimage[…]=-` for missing slots).

    Image refs that come back as `<basename>.<row>.<col>` (no `.<season>`
    suffix on the file stem) are addressed against the upstream PNG by
    integer `(row, col)` cell coords; sub-atlases / `frontimage` are
    ignored — the diff targets `backimage` only."""
    import re

    from pak.dat import parse

    objects = parse(dat_path)
    if not objects:
        raise SystemExit(f"empty dat: {dat_path}")
    # Building dats hold one obj=building entry in this codebase.
    obj = objects[0]
    rec = re.compile(
        r"^backimage"
        r"\[(\d+)\]\[(\d+)\]\[(\d+)\]\[(\d+)\]\[(\d+)\]\[(\d+)\]$",
    )
    ref = re.compile(r"\.(\d+)\.(\d+)\s*$")
    entries: list[dict] = []
    for k, v in obj:
        m = rec.match(k.lower())
        if not m:
            continue
        n = ref.search(v.strip())
        if not n:
            continue
        l, y, x, h, p, s = (int(g) for g in m.groups())
        row, col = int(n.group(1)), int(n.group(2))
        entries.append(dict(l=l, y=y, x=x, h=h, phase=p, season=s,
                            row=row, col=col))
    return entries


def _atlas_cell(atlas, row: int, col: int):
    """Return the 128×128 RGBA cell at `(row, col)` of `atlas` (H,W,4
    numpy array).  Raises with a clear message when the cell is out of
    range — saves debugging an opaque IndexError on a stale dat."""
    H, W = atlas.shape[:2]
    if (row + 1) * 128 > H or (col + 1) * 128 > W:
        raise SystemExit(
            f"atlas {W}×{H} lacks cell ({row}, {col}); "
            f"need at least {(col + 1) * 128}×{(row + 1) * 128}"
        )
    return atlas[row * 128:(row + 1) * 128, col * 128:(col + 1) * 128]


def _upstream_dat_path(upstream_stem: str) -> str:
    """Map an `upstream_stem` PNG path to the sibling dat path.
    Britain convention is `<dir>/images/<asset>.png` ←→ `<dir>/<asset>.dat`.
    Bare `<dir>/<asset>.png` (no `images/` subdir) maps to
    `<dir>/<asset>.dat`."""
    from pathlib import PurePosixPath

    p = PurePosixPath(upstream_stem)
    asset = p.stem
    if p.parent.name == "images":
        return str(p.parent.parent / f"{asset}.dat")
    return str(p.parent / f"{asset}.dat")


@dataclass(frozen=True)
class MultiTileCell:
    """One row of `run_multitile`'s report — the per-cell key plus the
    atlas coordinates we found on each side and the cross-projection
    silhouette IoU.  Atlas coords let a caller open the source PNG and
    locate the cell when a number looks off."""
    l: int
    y: int
    x: int
    h: int
    phase: int
    season: int
    our_row: int
    our_col: int
    up_row: int
    up_col: int
    iou: float

    @property
    def label(self) -> str:
        """Per-cell key string shared between the grid label and the
        text table — keeps grid + table in lockstep when phase/season
        cells eventually arrive."""
        return (f"L{self.l} y{self.y} x{self.x} h{self.h} "
                f"p{self.phase} s{self.season}")


def format_multitile_table(rows: list[MultiTileCell]) -> str:
    """Aligned text table for `run_multitile`'s per-cell report."""
    if not rows:
        return ""
    head = (
        f"  {'cell':<18}  {'ours':>7}  {'upstream':>9}  {'IoU':>5}"
    )
    body = [
        f"  {r.label:<18}  "
        f"{r.our_row:>2}.{r.our_col:<4}  "
        f"{r.up_row:>4}.{r.up_col:<4}  "
        f"{r.iou:>5.3f}"
        for r in rows
    ]
    ious = [r.iou for r in rows]
    summary = (
        f"  {'min/mean/max':<18}  {'':>7}  {'':>9}  "
        f"{min(ious):.3f} / {sum(ious) / len(ious):.3f} / {max(ious):.3f}"
    )
    return "\n".join([head, *body, summary])


def run_multitile(
    upstream_stem: str, our_dat: Path, our_png: Path, *, out_dir: Path,
    season: int = 0,
):
    """Per-cell visual diff for a multi-tile building.

    Reads upstream's dat (source of truth on which `(l,y,x,h,phase,
    season)` cells exist and where they land in the atlas) and our
    own emitted dat (which `iter_building_cells` produced for our hex
    bake), slices both atlases, composes a per-cell side-by-side grid
    at `out_dir/grid.png`, and returns a list of `MultiTileCell`
    records for the text report.

    No rendering — both sides come from committed atlases, so the path
    is a regression check against what we ship, not a calibration of
    what we'd re-bake.  Per-cell IoU is cross-projection (ours hex,
    upstream square dimetric); useful as a relative ranking across
    cells, not a FAIL_IOU gate.  See the module docstring + the TODO
    "Closed (not pursued)" entry for why absolute calibration against
    the shipped multi-tile atlas isn't a reachable target.
    """
    import numpy as np
    from PIL import Image

    from pak.diff import GridCell, compose_grid
    from pak.fetch_pak import fetch as fetch_pak

    out_dir.mkdir(parents=True, exist_ok=True)
    up_dat_path = fetch_pak(_upstream_dat_path(upstream_stem))
    up_png_path = fetch_pak(upstream_stem)
    up_atlas = np.asarray(Image.open(up_png_path).convert("RGBA"))
    our_atlas = np.asarray(Image.open(our_png).convert("RGBA"))

    def index(entries):
        return {(e["l"], e["y"], e["x"], e["h"], e["phase"], e["season"]):
                (e["row"], e["col"]) for e in entries}

    up_index = index(_parse_backimage_entries(up_dat_path))
    our_index = index(_parse_backimage_entries(our_dat))

    # Restrict to the requested season; our bake doesn't ship winter
    # yet, so seasons that exist upstream but not in our atlas drop.
    keys = sorted(
        k for k in up_index if k in our_index and k[5] == season
    )
    if not keys:
        raise SystemExit(
            f"no overlapping (l,y,x,h,phase,season={season}) cells "
            f"between upstream {up_dat_path.name} and our {our_dat.name}"
        )

    cells: list[GridCell] = []
    rows: list[MultiTileCell] = []
    for k in keys:
        our_r, our_c = our_index[k]
        up_r, up_c = up_index[k]
        up_cell = _atlas_cell(up_atlas, up_r, up_c)
        our_cell = _atlas_cell(our_atlas, our_r, our_c)
        our_mask = _silhouette_mask(our_cell)
        up_mask = _silhouette_mask(up_cell)
        l, y, x, h, p, s = k
        row = MultiTileCell(
            l=l, y=y, x=x, h=h, phase=p, season=s,
            our_row=our_r, our_col=our_c,
            up_row=up_r, up_col=up_c,
            iou=iou(our_mask, up_mask),
        )
        rows.append(row)
        cells.append(GridCell(
            ours_rgba=our_cell, up_rgba=up_cell,
            our_mask=our_mask, up_mask=up_mask,
            label=row.label,
        ))
    compose_grid(cells, out_path=out_dir / "grid.png",
                 strip_magic_rgb=MAGIC_PINK,
                 title=f"{our_dat.stem} (season {season})")
    return rows


def _load_our_renders(our_dir: Path, name: str, layouts: int):
    """Per-layout RGBA arrays produced by `_render`."""
    import numpy as np
    from PIL import Image

    return [
        np.asarray(
            Image.open(our_dir / f"{name}_L{l}_Y0_X0_H0.png").convert("RGBA")
        )
        for l in range(layouts)
    ]


def _iou_matrix(our_masks, up_masks):
    """N x N silhouette IoU matrix (rows = our layout, cols = upstream col)."""
    import numpy as np

    n = len(our_masks)
    mat = np.zeros((n, n), dtype=np.float64)
    for l in range(n):
        for c in range(n):
            mat[l, c] = iou(our_masks[l], up_masks[c])
    return mat


def _best_permutation(mat) -> list[int]:
    """Permutation `[c0, c1, ...]` maximising `sum(mat[i, ci])`.
    Enumerates all N! permutations -- `_UPSTREAM_NORMAL_CARDINAL`
    caps `layouts` at 4 (24 perms), so brute force is both optimal
    and dirt cheap."""
    n = mat.shape[0]
    best_perm, best_score = None, -1.0
    for perm in itertools.permutations(range(n)):
        score = sum(mat[i, perm[i]] for i in range(n))
        if score > best_score:
            best_perm, best_score = perm, score
    return list(best_perm)


def _diff_one_season(blend: str, upstream_png: str, *, layouts: int,
                     out_dir: Path, materials, season_row: int,
                     blur_sigma: float, lighting,
                     row_label_prefix: str = ""):
    """Render `blend`, diff each layout against the `season_row` row
    of `upstream_png`, and return `(grid_cells, mat, perm, drgb)`.

    `row_label_prefix` is prepended to each `GridCell.label` so a
    seasonal caller can disambiguate `summer L0` from `winter L0` in
    a combined grid.
    """
    from pak.diff import GridCell
    from pak.fetch_blend import fetch as fetch_blend
    from pak.fetch_pak import fetch as fetch_pak

    out_dir.mkdir(parents=True, exist_ok=True)
    blend_path = fetch_blend(blend)
    render_name = Path(blend).stem
    _render(blend_path, out_dir, render_name, layouts,
            materials=materials, lighting=lighting)
    up_path = fetch_pak(upstream_png)
    up_cells = _split_upstream(up_path, layouts, season_row=season_row)
    our_rgba = _load_our_renders(out_dir, render_name, layouts)
    our_masks = [_silhouette_mask(r) for r in our_rgba]
    up_masks = [_silhouette_mask(c) for c in up_cells]
    mat = _iou_matrix(our_masks, up_masks)
    perm = _best_permutation(mat)
    drgb_per_layout = [
        drgb_intersection(our_rgba[l], up_cells[perm[l]],
                          our_masks[l], up_masks[perm[l]],
                          blur_sigma=blur_sigma)
        for l in range(len(our_rgba))
    ]
    cells = [
        GridCell(our_rgba[i], up_cells[perm[i]],
                 our_masks[i], up_masks[perm[i]],
                 f"{row_label_prefix}L{i}~c{perm[i]}")
        for i in range(len(our_rgba))
    ]
    return cells, mat, perm, drgb_per_layout


def run(blend: str, upstream_png: str, *, layouts: int, out_dir: Path,
        materials: dict | None = None, season_row: int = 0,
        grid_name: str = "grid.png", blur_sigma: float = 3.0,
        lighting=None, title: str | None = None):
    """Render `blend` through `square_building`, diff each layout
    against `upstream_png`'s columns, return (matrix, permutation, drgb).

    `season_row` picks which 128-px row of the upstream atlas to diff
    against (0 = summer, 1 = winter).  Caller pre-selects the matching
    `blend` / `materials` for the season being checked.

    Side effect: writes per-layout PNGs and `<grid_name>` into `out_dir`.
    """
    from pak.diff import compose_grid

    cells, mat, perm, drgb_per_layout = _diff_one_season(
        blend, upstream_png, layouts=layouts, out_dir=out_dir,
        materials=materials, season_row=season_row,
        blur_sigma=blur_sigma, lighting=lighting,
    )
    compose_grid(cells, out_path=out_dir / grid_name,
                 strip_magic_rgb=MAGIC_PINK, title=title)
    return mat, perm, drgb_per_layout


def run_seasonal(
    blend: str, upstream_png: str, *, layouts: int, out_dir: Path,
    materials: dict | None = None,
    blend_winter: str, materials_winter: dict | None = None,
    lighting=None, blur_sigma: float = 3.0,
):
    """Diff summer then winter against the matching upstream rows and
    write **one** combined grid (`grid.png`) covering both seasons —
    summer rows first, winter rows below, labelled.  Returns a list of
    `(season_label, mat, perm, drgb)` so per-season IoU / permutation /
    dRGB stay separately reportable."""
    from pak.diff import compose_grid

    summer_cells, *summer_stats = _diff_one_season(
        blend, upstream_png, layouts=layouts, out_dir=out_dir,
        materials=materials, season_row=0,
        blur_sigma=blur_sigma, lighting=lighting,
        row_label_prefix="summer ",
    )
    winter_cells, *winter_stats = _diff_one_season(
        blend_winter, upstream_png, layouts=layouts, out_dir=out_dir,
        materials=materials_winter, season_row=1,
        blur_sigma=blur_sigma, lighting=lighting,
        row_label_prefix="winter ",
    )
    compose_grid(
        summer_cells + winter_cells,
        out_path=out_dir / "grid.png",
        strip_magic_rgb=MAGIC_PINK,
        title=f"{Path(blend).stem} (summer + winter)",
    )
    return [("summer", *summer_stats), ("winter", *winter_stats)]


def format_matrix(mat, perm) -> str:
    lines = []
    layouts = mat.shape[0]
    header = "        " + "  ".join(f"up_c{c:>1}" for c in range(layouts))
    lines.append(header)
    for l in range(layouts):
        row_vals = "  ".join(
            f"{mat[l, c]:>5.3f}" + ("*" if perm[l] == c else " ")
            for c in range(layouts)
        )
        lines.append(f"  our_L{l}  {row_vals}")
    return "\n".join(lines)


def summarise(mat, perm) -> tuple[float, float, float]:
    """`(worst_of_best, mean_best, mean_identity)`.  `mean_best` is
    the headline number; `worst_of_best` is what trips `FAIL_IOU`;
    `mean_identity` lets the caller see how much the permutation is
    actually buying over the trivial mapping."""
    n = mat.shape[0]
    best_vals = [mat[i, perm[i]] for i in range(n)]
    diag_vals = [mat[i, i] for i in range(n)]
    return min(best_vals), sum(best_vals) / n, sum(diag_vals) / n


def _parse(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("blend")
    ap.add_argument("upstream_png")
    ap.add_argument("--layouts", type=int, default=4)
    ap.add_argument("--out", default=None)
    return ap.parse_args(argv)


def main(argv) -> int:
    args = _parse(argv)
    stem = Path(args.blend).stem
    out_dir = Path(args.out) if args.out else REPO_ROOT / "out" / "diff" / stem
    mat, perm, drgb = run(args.blend, args.upstream_png, layouts=args.layouts, out_dir=out_dir)
    worst, best, diag = summarise(mat, perm)
    print(format_matrix(mat, perm))
    print(f"\nmean IoU identity: {diag:.3f}  best perm: {best:.3f}  perm={perm}")
    print(f"worst-of-best: {worst:.3f}  (FAIL_IOU={FAIL_IOU:.2f})")
    drgb_mean = sum(drgb) / len(drgb)
    drgb_max = max(drgb)
    print(f"dRGB (blurred all-pixel): mean={drgb_mean:.2f}  max={drgb_max:.2f}  "
          f"per-layout={[round(v, 2) for v in drgb]}")
    return 0 if worst >= FAIL_IOU else 1


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.exit(main(sys.argv[1:]))
