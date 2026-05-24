"""Remap upstream 2D-only buildings (no `.blend`) onto the hex tile lattice.

Stitch sq-dimetric cells via `pak.sq_split.stitch`, re-slice via
`pak.hex_split.split` onto a 4-hex rhombus.  Wrapped by the
`UpstreamRemap` sprite provider in `pak.sprites`; bake scripts that
use it declare `sprites=UpstreamRemap(...)` on their `Building`
SPEC.  The policy gap and the pink-ring / camera-mismatch artefacts
are in TODO.md → "2D-remap for blendless buildings".
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from pak import dat as _dat
from pak.fetch_pak import fetch as fetch_pak
from pak.hex_split import hex_tile_screen_offset, split as hex_split
from pak.sq_split import cell_anchors as sq_anchors, stitch as sq_stitch

W = 128
MAGIC_PINK = (231, 255, 255)

# Three 4-hex rhombus orientations, named after the orientation of the
# shared interior edge whose midpoint is the cluster centroid.  All C2-
# symmetric about that midpoint; geometrically congruent (rotated 60°
# from each other).
RHOMBUS_ORIENTATIONS: dict[str, list[tuple[int, int]]] = {
    "horizontal": [(0, 0), (0, 1), (1, 0), (-1, 1)],
    "slash":      [(0, 0), (1, 0), (0, 1), (1, 1)],
    "backslash":  [(0, 0), (1, 0), (0, 1), (1, -1)],
}


def _open_atlas(path: str) -> np.ndarray:
    cached = fetch_pak(path)
    return np.asarray(Image.open(cached).convert("RGBA"))


def _crop_cell(atlas: np.ndarray, row: int, col: int) -> np.ndarray:
    return atlas[row * W:(row + 1) * W, col * W:(col + 1) * W].copy()


def _stitch_sq(cells_yx: dict[tuple[int, int], np.ndarray],
               canvas_size: int = 512) -> np.ndarray:
    """Stitch sq-dimetric cells onto a canvas via `pak.sq_split.stitch`.

    Footprint centroid lands at the canvas centre; `sq_split` handles the
    ground-anchor offset inside each 128² sprite and the PINK-keyed paste.
    """
    cells_yxh = {(y, x, 0): cell for (y, x), cell in cells_yx.items()}
    anchors_raw = sq_anchors(cells_yxh)
    cc = canvas_size // 2
    anchors = {k: (a[0] + cc, a[1] + cc) for k, a in anchors_raw.items()}
    canvas = np.empty((canvas_size, canvas_size, 4), dtype=np.uint8)
    canvas[..., :3] = MAGIC_PINK
    canvas[..., 3] = 255
    sq_stitch(cells_yxh, anchors, into_canvas=canvas)
    return canvas


def _split_hex(stitched: np.ndarray,
               orientation: str) -> list[np.ndarray]:
    """Cut the stitched canvas into 4 hex cells via `pak.hex_split.split`.

    Per-cell axial keys anchor each 128² sprite at its hex screen offset
    relative to the cluster centroid; the cutter handles overlap and
    bottom-trim against the hex polygon.
    """
    cells = RHOMBUS_ORIENTATIONS[orientation]
    offsets = [hex_tile_screen_offset(q, r) for q, r in cells]
    cent_x = sum(o[0] for o in offsets) / len(offsets)
    cent_y = sum(o[1] for o in offsets) / len(offsets)
    ccx, ccy = stitched.shape[1] // 2, stitched.shape[0] // 2
    anchors = {
        (q, r, 0): (int(round(ox - cent_x)) + ccx,
                    int(round(oy - cent_y)) + ccy)
        for (q, r), (ox, oy) in zip(cells, offsets, strict=True)
    }
    out_cells = hex_split(stitched, anchors, image_width=W)
    return [out_cells[(q, r, 0)] for q, r in cells]


def _backimage_cells(obj_pairs: list[tuple[str, str]],
                     *, layout: int, season: int
                     ) -> dict[tuple[int, int], tuple[str, int, int]]:
    out: dict[tuple[int, int], tuple[str, int, int]] = {}
    for k, v in obj_pairs:
        if not k.lower().startswith("backimage"):
            continue
        idxs = [int(p.rstrip("]")) for p in k.split("[")[1:]]
        L, y, x, h, phase, s = idxs
        if (L, h, phase, s) != (layout, 0, 0, season):
            continue
        head, _, col_str = v.rpartition(".")
        stem, _, row_str = head.rpartition(".")
        out[(y, x)] = (stem, int(row_str), int(col_str))
    if not out:
        raise SystemExit(f"no backimage for L={layout} season={season}")
    return out


def remap_to_cells(dat_path: Path, name: str, *,
                   layout: int, season: int, orientation: str,
                   ) -> tuple[list[np.ndarray], np.ndarray]:
    """In-memory remap.  Returns `(hex_cells, stitched)` — hex_cells is
    a list of 4 RGBA ndarrays in `RHOMBUS_ORIENTATIONS[orientation]`
    axial order; stitched is the 512² intermediate (for diagnostics)."""
    obj_pairs = next(
        (obj for obj in _dat.parse(dat_path)
         if any(k.lower() == "name" and v == name for k, v in obj)),
        None,
    )
    if obj_pairs is None:
        raise SystemExit(f"object Name={name!r} not found in {dat_path}")

    refs = _backimage_cells(obj_pairs, layout=layout, season=season)
    class_dir = dat_path.parent.name
    stem = next(iter(refs.values()))[0]
    atlas = _open_atlas(f"{class_dir}/{stem}.png")

    cells_yx = {(y, x): _crop_cell(atlas, row, col)
                for (y, x), (_, row, col) in refs.items()}
    stitched = _stitch_sq(cells_yx)
    hex_cells = _split_hex(stitched, orientation)
    return hex_cells, stitched


def remap_one(dat_path: Path, name: str, *, layout: int, season: int,
              orientation: str, out_png: Path,
              dump_stitched: bool = False) -> None:
    hex_cells, stitched = remap_to_cells(
        dat_path, name, layout=layout, season=season, orientation=orientation,
    )
    out_atlas = np.concatenate(hex_cells, axis=1)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(out_atlas).save(out_png)
    if dump_stitched:
        Image.fromarray(stitched).save(out_png.with_suffix(".stitched.png"))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dat", type=Path)
    ap.add_argument("name", help="object Name= field in the dat")
    ap.add_argument("--orientation", choices=list(RHOMBUS_ORIENTATIONS),
                    default="horizontal")
    ap.add_argument("--layout", type=int, default=0)
    ap.add_argument("--season", type=int, default=0)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--dump-stitched", action="store_true",
                    help="also write <out>.stitched.png for inspection")
    args = ap.parse_args(argv)
    remap_one(args.dat, args.name,
              layout=args.layout, season=args.season,
              orientation=args.orientation,
              out_png=args.out, dump_stitched=args.dump_stitched)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
