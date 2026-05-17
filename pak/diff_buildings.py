"""Building calibration: render a building blend through the square
viewpoint and pixel-diff each layout against the upstream pakset atlas.

Mirrors `diff_upstream.py` for buildings, with two differences from the
vehicle harness:

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

Today's scope: single-tile (dims_x = dims_y = heights = 1) buildings
only.  Multi-tile per-cell diffs need a square tile lattice analogous
to the hex `HEX_KOORD_Q_WORLD`; see TODO.md.

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


def _compose_grid(our_rgba, up_cells, our_masks, up_masks,
                  perm: list[int], out_path: Path) -> None:
    """Three-row grid (ours / upstream-best-match / silhouette XOR) so
    contour drift is visible at a glance.  Same shape as
    `diff_upstream.py::_compose`'s output."""
    from PIL import Image, ImageDraw

    from pak.diff import checker, xor_image

    CELL, PAD, LH = 128, 8, 18
    cols, rows = len(our_rgba), 3
    W = cols * (CELL + PAD) + PAD
    H = rows * (CELL + PAD) + PAD + LH

    bg = checker(CELL)
    grid = Image.new("RGBA", (W, H), (245, 245, 245, 255))
    draw = ImageDraw.Draw(grid)

    for i, (ours, up_idx) in enumerate(zip(our_rgba, perm)):
        label = f"L{i}~c{up_idx}"
        draw.text((PAD + i * (CELL + PAD) + 4, 2), label, fill=(0, 0, 0, 255))
        # Strip magic-pink before pasting upstream cell so the
        # checker background reads through.
        up_cell = up_cells[up_idx].copy()
        pink = ((up_cell[..., 0] == MAGIC_PINK[0])
                & (up_cell[..., 1] == MAGIC_PINK[1])
                & (up_cell[..., 2] == MAGIC_PINK[2]))
        up_cell[pink, 3] = 0
        x = PAD + i * (CELL + PAD)
        grid.paste(Image.alpha_composite(bg, Image.fromarray(ours, "RGBA")),
                   (x, LH + PAD))
        grid.paste(Image.alpha_composite(bg, Image.fromarray(up_cell, "RGBA")),
                   (x, LH + PAD + CELL + PAD))

        grid.paste(Image.fromarray(xor_image(our_masks[i], up_masks[up_idx]),
                                   "RGBA"),
                   (x, LH + PAD + 2 * (CELL + PAD)))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    grid.save(out_path)


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


def run(blend: str, upstream_png: str, *, layouts: int, out_dir: Path,
        materials: dict | None = None, season_row: int = 0,
        grid_name: str = "grid.png", blur_sigma: float = 3.0,
        lighting=None):
    """Render `blend` through `square_building`, diff each layout
    against `upstream_png`'s columns, return (matrix, permutation, drgb).

    `season_row` picks which 128-px row of the upstream atlas to diff
    against (0 = summer, 1 = winter).  Caller pre-selects the matching
    `blend` / `materials` for the season being checked.

    Side effect: writes per-layout PNGs and `<grid_name>` into `out_dir`.
    """
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
    _compose_grid(our_rgba, up_cells, our_masks, up_masks, perm,
                  out_dir / grid_name)
    return mat, perm, drgb_per_layout


def run_seasonal(
    blend: str, upstream_png: str, *, layouts: int, out_dir: Path,
    materials: dict | None = None,
    blend_winter: str, materials_winter: dict | None = None,
    lighting=None,
):
    """Run `run()` once per season and return a list of
    `(season_label, mat, perm, drgb)` — `("summer", ...)` first, then
    `("winter", ...)`.  Each season writes its own grid PNG so the two
    diffs can be eyeballed side by side."""
    summer = run(
        blend, upstream_png, layouts=layouts, out_dir=out_dir,
        materials=materials, season_row=0, grid_name="grid_summer.png",
        lighting=lighting,
    )
    winter = run(
        blend_winter, upstream_png, layouts=layouts, out_dir=out_dir,
        materials=materials_winter, season_row=1, grid_name="grid_winter.png",
        lighting=lighting,
    )
    return [("summer", *summer), ("winter", *winter)]


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
