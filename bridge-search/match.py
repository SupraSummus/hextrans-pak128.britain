"""Score every candidate blend facing against every upstream bridge cell.

Loads each candidate atlas (one row of 8 facings) and slices each upstream
atlas into its 128x128 cells.  For each (candidate_facing, upstream_cell)
pair, computes silhouette IoU after recentering both masks to their bbox
centroid; reports the top-K matches per upstream cell to stdout, and
optionally writes a visualisation grid.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

CELL = 128
ALPHA_THRESHOLD = 16   # match diff_upstream's convention for vehicles
MAGIC_PINK = (231, 255, 255)  # upstream pak's transparency colour

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PAK_SHA = "e36ec2321681baa06654be06e4b169965c0beec9"  # pak.lock commit
PAK_CACHE = REPO / ".cache/pak" / PAK_SHA


def load_atlas_rgba(path: Path) -> np.ndarray:
    im = Image.open(path).convert("RGBA")
    return np.asarray(im)


def upstream_silhouette(cell_rgba: np.ndarray) -> np.ndarray:
    """Upstream pak PNGs use magic-pink (231,255,255) for transparency
    (no alpha channel); cells already converted to RGBA above will have
    full alpha everywhere.  Mask = (RGB != MAGIC_PINK) on any channel."""
    rgb = cell_rgba[..., :3]
    pink = np.array(MAGIC_PINK, dtype=np.uint8)
    return np.any(rgb != pink, axis=-1)


def render_silhouette(cell_rgba: np.ndarray) -> np.ndarray:
    """Renders from pak/render.py carry true alpha (film_transparent=True)."""
    return cell_rgba[..., 3] > ALPHA_THRESHOLD


def bbox_of(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def recenter(mask: np.ndarray) -> np.ndarray:
    """Translate mask so its bbox centre lands at image centre.  Keeps
    scale and aspect — only fixes the per-cell anchor offset that
    differs between square dat (`,0,32` shift) and our render."""
    bb = bbox_of(mask)
    if bb is None:
        return mask
    x0, y0, x1, y1 = bb
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    H, W = mask.shape
    dx = int(round(W / 2.0 - cx))
    dy = int(round(H / 2.0 - cy))
    out = np.zeros_like(mask)
    sx0 = max(0, dx); sy0 = max(0, dy)
    ex0 = max(0, -dx); ey0 = max(0, -dy)
    w = min(W - sx0, W - ex0)
    h = min(H - sy0, H - ey0)
    if w > 0 and h > 0:
        out[sy0:sy0 + h, sx0:sx0 + w] = mask[ey0:ey0 + h, ex0:ex0 + w]
    return out


def iou(a: np.ndarray, b: np.ndarray) -> float:
    inter = np.logical_and(a, b).sum()
    union = np.logical_or(a, b).sum()
    return inter / union if union > 0 else 0.0


def slice_atlas(rgba: np.ndarray) -> list[tuple[str, np.ndarray]]:
    H, W = rgba.shape[:2]
    rows = H // CELL
    cols = W // CELL
    cells = []
    for r in range(rows):
        for c in range(cols):
            cell = rgba[r * CELL:(r + 1) * CELL, c * CELL:(c + 1) * CELL]
            cells.append((f"{r}.{c}", cell))
    return cells


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--candidates", default=str(HERE / "renders"),
                    help="dir holding *_sq.png atlases")
    ap.add_argument("--top-k", type=int, default=3,
                    help="how many candidate facings to keep per upstream cell")
    ap.add_argument("--min-iou", type=float, default=0.55,
                    help="don't print upstream cells whose best match falls below this")
    ap.add_argument("--out-grid", type=Path, default=None,
                    help="optional: write a top-1 comparison grid for the upstream "
                         "cells whose best match >= --min-iou-grid")
    ap.add_argument("--min-iou-grid", type=float, default=0.70)
    args = ap.parse_args()

    # Candidate atlases: row of 8 facings, names S/SW/W/NW/N/NE/E/SE.
    FACINGS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
    cand_dir = Path(args.candidates)
    cand_atlases = sorted(cand_dir.glob("*_sq.png"))
    if not cand_atlases:
        raise SystemExit(f"no *_sq.png under {cand_dir}")

    candidates: list[tuple[str, np.ndarray]] = []  # (label, recentered mask)
    cand_originals: dict[str, np.ndarray] = {}
    for p in cand_atlases:
        rgba = load_atlas_rgba(p)
        for i, f in enumerate(FACINGS):
            cell = rgba[0:CELL, i * CELL:(i + 1) * CELL]
            mask = render_silhouette(cell)
            label = f"{p.stem}/{f}"
            cand_originals[label] = cell
            if mask.sum() < 20:
                continue  # skip empty/near-empty facings
            candidates.append((label, recenter(mask)))

    print(f"# loaded {len(candidates)} candidate facings (skipped empties)")

    # Upstream atlases: every PNG in cache directory.
    up_dir = PAK_CACHE / "ways/images"
    up_paths = sorted(up_dir.glob("*.png"))
    if not up_paths:
        raise SystemExit(f"no PNGs under {up_dir} — fetch first")

    print(f"# scanning {len(up_paths)} upstream atlases")

    # For each upstream cell, find top-K candidate facings.
    results: list[tuple[float, str, str]] = []  # (iou, upstream_id, cand_label)
    grid_rows: list[tuple[str, np.ndarray, list[tuple[float, str]]]] = []

    for up_path in up_paths:
        rgba = load_atlas_rgba(up_path)
        for cell_id, cell in slice_atlas(rgba):
            mask = upstream_silhouette(cell)
            if mask.sum() < 1500:
                continue  # skip blanks AND icon/cursor cells (typ. < 1k px)
            mask_rc = recenter(mask)
            scored = []
            for label, c_mask in candidates:
                scored.append((iou(mask_rc, c_mask), label))
            scored.sort(reverse=True)
            top = scored[:args.top_k]
            up_id = f"{up_path.stem}.{cell_id}"
            if top[0][0] >= args.min_iou:
                results.append((top[0][0], up_id, ", ".join(f"{io:.3f} {lab}" for io, lab in top)))
            if top[0][0] >= args.min_iou_grid:
                grid_rows.append((up_id, cell, top))

    results.sort(reverse=True)
    print(f"\n# {len(results)} upstream cells with best IoU >= {args.min_iou}")
    print("# upstream_cell".ljust(50), "top-k (iou label)")
    for _, up_id, tops in results[:80]:
        print(f"{up_id:<50s} {tops}")

    if args.out_grid and grid_rows:
        cols = 1 + args.top_k
        rows = len(grid_rows)
        out = Image.new("RGB", (CELL * cols, CELL * rows), (255, 255, 255))
        for r, (up_id, up_cell, top) in enumerate(grid_rows):
            # upstream cell -> col 0, composited onto white via magic-pink mask
            mask = upstream_silhouette(up_cell)
            up_rgb = up_cell[..., :3].copy()
            up_rgb[~mask] = 255
            out.paste(Image.fromarray(up_rgb), (0, r * CELL))
            for k, (iou_v, cand_label) in enumerate(top):
                cand = cand_originals[cand_label]
                bg = Image.new("RGB", (CELL, CELL), (255, 255, 255))
                bg.paste(Image.fromarray(cand), mask=Image.fromarray(cand).split()[3])
                out.paste(bg, ((k + 1) * CELL, r * CELL))
        out = out.resize((out.width * 4, out.height * 4), Image.NEAREST)
        out.save(args.out_grid)
        print(f"\n# wrote grid: {args.out_grid}  ({len(grid_rows)} upstream cells, top-{args.top_k})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
