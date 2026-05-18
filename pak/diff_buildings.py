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

`run_multitile` is the multi-tile path — renders the blend through
the multi-tile `square_building` viewpoint (one full-canvas Facing
per layout at 512²) and compares against upstream's per-cell PNGs
on the same tile lattice.  Two grids drop out:

  * `grid_tiles.png` — one row per (L, y, x).  Our cell is the
    128×128 crop of our 512² render at the tile screen offset;
    upstream's is its committed atlas cell at the dat-referenced
    (row, col).
  * `grid_stitched.png` — one row per layout on the full 512²
    canvas.  Upstream's per-cell PNGs paste onto a 512² magic-pink
    canvas at the same tile lattice; ours is the render unchanged.

Both axes are single-projection (square vs square), so IoU + dRGB
are calibration-grade rather than cross-projection.  See TODO.md →
"Multi-tile calibration diff residual position offset" for the
current residual + the diagnostic next moves.

Run via the more ergonomic `pak/check.py` driver (which reads `blend`
and `upstream_dat` from the SPEC), or directly:

    python3 -m pak.diff_buildings \\
        <blend_path_in_blends_repo> \\
        <upstream_dat_path_in_pak_repo> \\
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
from pak.dat import building_footprint_centroid
from pak.diff import MAGIC_PINK, cell_metric, drgb_intersection, iou, silhouette_mask

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


def _cell_metric(ours_rgba, up_rgba, *, blur_sigma: float = 3.0):
    """Per-class wrapper around `pak.diff.cell_metric` that pins the
    building convention (`alpha_threshold=0`, `magic_rgb=MAGIC_PINK`).
    Returns `(CellMetric, our_mask, up_mask)`."""
    return cell_metric(
        ours_rgba, up_rgba,
        alpha_threshold=0, magic_rgb=MAGIC_PINK,
        blur_sigma=blur_sigma,
    )


def _render(blend_path: Path, out_dir: Path, name: str, layouts: int,
            *, dims_x: int = 1, dims_y: int = 1,
            materials: dict | None = None, lighting=None) -> None:
    script = HERE / "render.py"
    cmd = [
        "blender", "-b", str(blend_path), "-P", str(script), "--",
        "--out", str(out_dir), "--name", name,
        "--viewpoint", "square_building",
        "--building-footprint", f"{dims_x},{dims_y},{layouts},1",
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


def _parse_backimage_entries(dat_path: Path, *, name: str | None = None):
    """Parse a building dat's `backimage[L][y][x][h][p][s]=<basename>.<row>.<col>`
    entries.  Returns list of dicts with keys
    `l, y, x, h, phase, season, row, col`.  Ignores image refs that
    can't be parsed (e.g. `backimage[…]=-` for missing slots).

    `name` filters multi-object dats (citybuildings dats hold up to
    seven buildings); unset takes the first object.

    Image refs that come back as `<basename>.<row>.<col>` (no `.<season>`
    suffix on the file stem) are addressed against the upstream PNG by
    integer `(row, col)` cell coords; sub-atlases / `frontimage` are
    ignored — the diff targets `backimage` only."""
    import re

    from pak.dat import parse

    objects = parse(dat_path)
    if not objects:
        raise SystemExit(f"empty dat: {dat_path}")
    if name is None:
        obj = objects[0]
    else:
        wanted = name.lower()
        match = next(
            (o for o in objects
             if any(k.lower() == "name" and v.strip().lower() == wanted
                    for k, v in o)),
            None,
        )
        if match is None:
            raise SystemExit(f"no obj named {name!r} in {dat_path}")
        obj = match
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


# Simutrans Standard dimetric tile lattice: koord +x heads SE on screen,
# koord +y heads SW.  Multi-tile cells place at this offset around the
# building's koord (0, 0) origin.  Accepts floats so per-layout centroid
# shifts can use the same formula.
def _sq_tile_screen_offset(x: float, y: float) -> tuple[float, float]:
    return (64.0 * x - 64.0 * y, 32.0 * x + 32.0 * y)


# Per-layout square_building canvas size.  Camera looks at world origin,
# so world (0, 0, 0) -- the blend footprint centroid by the Britain
# contributing-graphics spec -- lands at the canvas centre.  The
# building's tiles fan out around that point per the engine paint
# convention encoded by `_tile_topleft`.
_SQ_CANVAS_W = _SQ_CANVAS_H = 512
_SQ_CANVAS_ORIGIN = (_SQ_CANVAS_W // 2, _SQ_CANVAS_H // 2)


# Pixel position of the tile's z=0 ground anchor within its 128×128 cell.
# Simutrans dimetric convention: ground sits at (64, 96) -- bottom of
# the diamond -- NOT cell centre.  Anchoring upstream cells at the
# ground point (rather than cell centre) matches where the engine
# paints them.
_CELL_GROUND_ANCHOR = (64, 96)


def _tile_topleft(x: int, y: int,
                  centroid_xy: tuple[float, float]) -> tuple[int, int]:
    """Top-left pixel of tile (y, x)'s 128×128 cell on the layout canvas.
    The cell's `_CELL_GROUND_ANCHOR` pixel lands at the engine
    `koord_to_screen` offset from `centroid_xy` (in koord units), so the
    building's footprint centres on canvas where our render anchors
    world (0, 0, 0)."""
    cx, cy = _SQ_CANVAS_ORIGIN
    xc, yc = centroid_xy
    ax, ay = _CELL_GROUND_ANCHOR
    dx, dy = _sq_tile_screen_offset(x - xc, y - yc)
    return (int(round(cx + dx)) - ax, int(round(cy + dy)) - ay)


def _crop_cell(canvas, x: int, y: int,
               centroid_xy: tuple[float, float]):
    """Crop the 128×128 cell for tile (y, x) from a 512×512 layout
    canvas, aligned to the same per-layout centroid the stitch uses."""
    x0, y0 = _tile_topleft(x, y, centroid_xy)
    return canvas[y0:y0 + 128, x0:x0 + 128]


def _stitch_upstream_layout(cells_by_yx, centroid_xy, *, magic_rgb):
    """Build a 512×512 RGBA canvas with each upstream 128×128 cell pasted
    at its tile (y, x) screen position around `centroid_xy`.  Background
    fills with `magic_rgb` so upstream's transparency convention
    survives stitch."""
    import numpy as np
    canvas = np.empty((_SQ_CANVAS_H, _SQ_CANVAS_W, 4), dtype=np.uint8)
    canvas[..., :3] = magic_rgb
    canvas[..., 3] = 255
    for (y, x), cell in cells_by_yx.items():
        x0, y0 = _tile_topleft(x, y, centroid_xy)
        keyed = (cell[..., :3] == magic_rgb).all(axis=-1)
        sub = canvas[y0:y0 + 128, x0:x0 + 128]
        sub[~keyed] = cell[~keyed]
    return canvas


@dataclass(frozen=True)
class MultiTileCell:
    """One per-(L, y, x, h, phase, season) cell metric.

    Both sides are square-projection (ours sliced from the
    `square_building` render at the tile screen offset; upstream from
    its committed per-cell PNG), so IoU and dRGB are calibration-grade
    rather than cross-projection."""
    l: int
    y: int
    x: int
    h: int
    phase: int
    season: int
    iou: float
    drgb: float

    @property
    def label(self) -> str:
        return (f"L{self.l} y{self.y} x{self.x} h{self.h} "
                f"p{self.phase} s{self.season}")


@dataclass(frozen=True)
class MultiTileLayout:
    """One per-layout stitched-canvas metric — full 512×512 silhouette
    IoU + colour over the whole footprint (no tile boundary crops)."""
    l: int
    iou: float
    drgb: float

    @property
    def label(self) -> str:
        return f"L{self.l} stitched"


def _format_metric_table(rows, label_w: int = 22) -> str:
    """Shared per-row aligned table; works for both `MultiTileCell` and
    `MultiTileLayout` (both expose `.label`, `.iou`, `.drgb`)."""
    if not rows:
        return ""
    head = f"  {'cell':<{label_w}}  {'IoU':>5}  {'dRGB':>5}"
    body = [
        f"  {r.label:<{label_w}}  {r.iou:>5.3f}  {r.drgb:>5.1f}"
        for r in rows
    ]
    ious = [r.iou for r in rows]
    drgbs = [r.drgb for r in rows]
    # Summary: worst IoU (what would gate FAIL_IOU) + mean dRGB
    # (calibration headline, mirrors `summarise` for the single-tile run).
    summary = (
        f"  {'worst / mean':<{label_w}}  "
        f"{min(ious):>5.3f}  {sum(drgbs) / len(drgbs):>5.1f}"
    )
    return "\n".join([head, *body, summary])


def format_multitile_table(rows: list[MultiTileCell]) -> str:
    """Aligned per-cell text table for `run_multitile`."""
    return _format_metric_table(rows)


def format_multitile_layout_table(rows: list[MultiTileLayout]) -> str:
    """Aligned per-layout text table for `run_multitile`'s stitched
    pass."""
    return _format_metric_table(rows, label_w=14)


def run_multitile(
    blend: str, upstream_dat: str, *,
    dims_x: int, dims_y: int, layouts: int,
    out_dir: Path,
    materials: dict | None = None,
    lighting=None,
    season: int = 0,
    blur_sigma: float = 3.0,
    name: str | None = None,
):
    """Render the multi-tile blend through `square_building`, build the
    per-layout stitched upstream canvas from upstream's per-cell PNGs,
    and emit two diff grids:

      * `grid_tiles.png` -- per-cell side-by-side, one row per (L, y, x)
        cell.  Our cell is the 128×128 crop of our 512×512 render at the
        tile (y, x) screen offset; upstream's is its committed cell.
      * `grid_stitched.png` -- per-layout side-by-side on the full
        512×512 canvas (ours unchanged, upstream's per-cell PNGs pasted
        onto a 512×512 magic-pink canvas at the same tile lattice).

    Both axes are square-vs-square so IoU and dRGB are absolute
    calibration metrics.  Returns `(per_cell, per_layout)` lists.

    `season` picks which upstream cells to compare against (0=summer).
    """
    import numpy as np
    from PIL import Image

    from pak.diff import GridCell, compose_grid
    from pak.fetch_blend import fetch as fetch_blend
    from pak.fetch_pak import fetch as fetch_pak
    from pak.upstream import image_stem

    out_dir.mkdir(parents=True, exist_ok=True)
    blend_path = fetch_blend(blend)
    render_name = Path(blend).stem
    _render(blend_path, out_dir, render_name, layouts,
            dims_x=dims_x, dims_y=dims_y,
            materials=materials, lighting=lighting)
    our_canvases = _load_our_renders(out_dir, render_name, layouts)

    up_dat_path = fetch_pak(upstream_dat)
    up_png_path = fetch_pak(f"{image_stem(upstream_dat, name=name)}.png")
    up_atlas = np.asarray(Image.open(up_png_path).convert("RGBA"))
    # Upstream cells indexed by (L, y, x, h, p, s) -> (row, col); the
    # requested season filters everything else out.
    up_index = {
        (e["l"], e["y"], e["x"], e["h"], e["phase"], e["season"]):
            (e["row"], e["col"])
        for e in _parse_backimage_entries(up_dat_path, name=name)
        if e["season"] == season
    }
    if not up_index:
        raise SystemExit(
            f"no upstream cells at season={season} in {up_dat_path.name}"
        )

    # Per-layout footprint centroid in (x, y) koord units, derived from
    # (dims_x, dims_y, L) -- the engine's even/odd `(y, x)` cell-range
    # swap in `building_writer.cc`.  Spec-side geometry; both passes use
    # it to centre the dat's tile lattice around our render's world
    # origin.
    centroid_by_L = {
        L: building_footprint_centroid(dims_x, dims_y, L)
        for L in range(layouts)
    }

    # Per-cell diff: one row per (L, y, x).  Our cell is the 128×128
    # crop of our 512×512 render at the tile screen offset; upstream's
    # is its committed atlas cell.
    per_cell: list[MultiTileCell] = []
    tile_grid_cells: list[GridCell] = []
    for k in sorted(up_index):
        l, y, x, h, p, s = k
        up_cell = _atlas_cell(up_atlas, *up_index[k])
        our_cell = _crop_cell(our_canvases[l], x, y, centroid_by_L[l])
        m, our_mask, up_mask = _cell_metric(our_cell, up_cell,
                                            blur_sigma=blur_sigma)
        rec = MultiTileCell(l=l, y=y, x=x, h=h, phase=p, season=s,
                            iou=m.iou, drgb=m.drgb)
        per_cell.append(rec)
        tile_grid_cells.append(GridCell(
            ours_rgba=our_cell, up_rgba=up_cell,
            our_mask=our_mask, up_mask=up_mask, label=rec.label,
        ))
    compose_grid(tile_grid_cells, out_path=out_dir / "grid_tiles.png",
                 strip_magic_rgb=MAGIC_PINK,
                 title=f"{render_name} per-tile (square)")

    # Per-layout stitched diff: one row per L on the full 512×512 canvas.
    # Upstream's per-cell PNGs paste onto the same tile lattice we sliced
    # ours from, so the silhouette IoU is apples-to-apples.
    per_layout: list[MultiTileLayout] = []
    stitched_cells: list[GridCell] = []
    for L in range(layouts):
        cells_by_yx = {
            (k[1], k[2]): _atlas_cell(up_atlas, *up_index[k])
            for k in up_index if k[0] == L
        }
        up_stitched = _stitch_upstream_layout(cells_by_yx, centroid_by_L[L],
                                              magic_rgb=MAGIC_PINK)
        m, our_mask, up_mask = _cell_metric(our_canvases[L], up_stitched,
                                            blur_sigma=blur_sigma)
        rec = MultiTileLayout(l=L, iou=m.iou, drgb=m.drgb)
        per_layout.append(rec)
        stitched_cells.append(GridCell(
            ours_rgba=our_canvases[L], up_rgba=up_stitched,
            our_mask=our_mask, up_mask=up_mask, label=rec.label,
        ))
    compose_grid(stitched_cells, out_path=out_dir / "grid_stitched.png",
                 strip_magic_rgb=MAGIC_PINK,
                 cell_px=_SQ_CANVAS_W,
                 title=f"{render_name} per-layout stitched")

    return per_cell, per_layout


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


def _diff_one_season(blend: str, upstream_dat: str, *, layouts: int,
                     out_dir: Path, materials, season_row: int,
                     blur_sigma: float, lighting,
                     row_label_prefix: str = "",
                     name: str | None = None):
    """Render `blend`, diff each layout against the `season_row` row
    of the upstream atlas (derived from `upstream_dat`'s `BackImage`
    refs), and return `(grid_cells, mat, perm, drgb)`.

    `row_label_prefix` is prepended to each `GridCell.label` so a
    seasonal caller can disambiguate `summer L0` from `winter L0` in
    a combined grid.
    """
    from pak.diff import GridCell
    from pak.fetch_blend import fetch as fetch_blend
    from pak.fetch_pak import fetch as fetch_pak
    from pak.upstream import image_stem

    out_dir.mkdir(parents=True, exist_ok=True)
    blend_path = fetch_blend(blend)
    render_name = Path(blend).stem
    _render(blend_path, out_dir, render_name, layouts,
            materials=materials, lighting=lighting)
    up_path = fetch_pak(f"{image_stem(upstream_dat, name=name)}.png")
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


def run(blend: str, upstream_dat: str, *, layouts: int, out_dir: Path,
        materials: dict | None = None, season_row: int = 0,
        grid_name: str = "grid.png", blur_sigma: float = 3.0,
        lighting=None, title: str | None = None,
        name: str | None = None):
    """Render `blend` through `square_building`, diff each layout
    against the columns of the upstream atlas (derived from
    `upstream_dat`'s `BackImage` refs), return (matrix, permutation, drgb).

    `season_row` picks which 128-px row of the upstream atlas to diff
    against (0 = summer, 1 = winter).  Caller pre-selects the matching
    `blend` / `materials` for the season being checked.

    Side effect: writes per-layout PNGs and `<grid_name>` into `out_dir`.
    """
    from pak.diff import compose_grid

    cells, mat, perm, drgb_per_layout = _diff_one_season(
        blend, upstream_dat, layouts=layouts, out_dir=out_dir,
        materials=materials, season_row=season_row,
        blur_sigma=blur_sigma, lighting=lighting, name=name,
    )
    compose_grid(cells, out_path=out_dir / grid_name,
                 strip_magic_rgb=MAGIC_PINK, title=title)
    return mat, perm, drgb_per_layout


def run_seasonal(
    blend: str, upstream_dat: str, *, layouts: int, out_dir: Path,
    materials: dict | None = None,
    blend_winter: str, materials_winter: dict | None = None,
    lighting=None, blur_sigma: float = 3.0,
    name: str | None = None,
):
    """Diff summer then winter against the matching upstream rows and
    write **one** combined grid (`grid.png`) covering both seasons —
    summer rows first, winter rows below, labelled.  Returns a list of
    `(season_label, mat, perm, drgb)` so per-season IoU / permutation /
    dRGB stay separately reportable."""
    from pak.diff import compose_grid

    summer_cells, *summer_stats = _diff_one_season(
        blend, upstream_dat, layouts=layouts, out_dir=out_dir,
        materials=materials, season_row=0,
        blur_sigma=blur_sigma, lighting=lighting,
        row_label_prefix="summer ", name=name,
    )
    winter_cells, *winter_stats = _diff_one_season(
        blend_winter, upstream_dat, layouts=layouts, out_dir=out_dir,
        materials=materials_winter, season_row=1,
        blur_sigma=blur_sigma, lighting=lighting,
        row_label_prefix="winter ", name=name,
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
    ap.add_argument("upstream_dat")
    ap.add_argument("--layouts", type=int, default=4)
    ap.add_argument("--out", default=None)
    return ap.parse_args(argv)


def main(argv) -> int:
    args = _parse(argv)
    stem = Path(args.blend).stem
    out_dir = Path(args.out) if args.out else REPO_ROOT / "out" / "diff" / stem
    mat, perm, drgb = run(args.blend, args.upstream_dat, layouts=args.layouts, out_dir=out_dir)
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
