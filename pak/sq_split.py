"""Square dimetric per-tile cutter.

Algorithm in `pak.cell_split`; this module supplies the square specifics:
`_bottom_triangles` for the ground polygon trim, dimetric `_paint_key`
for back-first order, `cell_anchors` over `(y, x, h)` keys.

Pinned pixel-exact against An-dz/tilecutter's 7 fixed masks on
OilRefinery1955 (`tests/test_sq_split.py::TestStitchSplitRefinery`,
4 layouts × 42 cells) -- the fixed masks are the closed-form lookup for
the partition the iteration computes under the dimetric projection.

For pak128 (`paksize=128`): `half=64`, `fourth=32`; ground anchor at
`(half, half + fourth) = (64, 96)` inside each 128² cell.
"""

from __future__ import annotations

import numpy as np

from pak import cell_split

W = 128
GROUND_ANCHOR = (64, 96)


def _bottom_triangles(paksize: int = W) -> np.ndarray:
    """The two bottom-corner triangles outside the diamond polygon.
    True = trim from ground-level cells' footprints.

    Per-row, with `dy = sprite_y - (half + fourth)`:
      * left triangle: `xs < 2 * dy`
      * right triangle: `xs >= paksize - 2 * dy`
    """
    half = paksize // 2
    fourth = paksize // 4
    ys, xs = np.indices((paksize, paksize))
    dy = ys - (half + fourth)
    bot = dy >= 0
    return bot & ((xs < 2 * dy) | (xs >= paksize - 2 * dy))


def _paint_key(k):
    """Back-first paint order under square dimetric: `(x + y)` is the
    tile depth proxy (both `+x` and `+y` push screen y down = closer to
    viewer); within tile, `h` ascending (h=0 first).  Ties broken by
    `(y, x)` for determinism."""
    y, x, h = k
    return (x + y, h, y, x)


def _is_ground(k):
    return k[2] == 0


def _lattice(paksize: int) -> cell_split.Lattice:
    return cell_split.Lattice(
        box=paksize,
        ground_anchor=(paksize // 2, 3 * paksize // 4),
        bottom_trim=_bottom_triangles(paksize),
        paint_key=_paint_key,
        is_ground=_is_ground,
    )


def cell_anchors(
    cells_yxh,
    *,
    footprint_center: tuple[float, float] | None = None,
    paksize: int = W,
) -> dict[tuple[int, int, int], tuple[int, int]]:
    """Map each `(y, x, h)` to its ground-anchor in a canvas frame
    whose origin sits at `(0, 0)`.  Caller adds a final shift to bring
    anchors into a positive-coordinate canvas (see `stitch`).  Heights
    stack at `paksize` px per `h` step (engine `ypos -= raster_width`
    paint loop in `obj/gebaeude.cc::display`)."""
    yxh = list(cells_yxh)
    if footprint_center is None:
        ys = [y for y, _, _ in yxh]
        xs = [x for _, x, _ in yxh]
        footprint_center = ((max(xs) + min(xs)) / 2,
                            (max(ys) + min(ys)) / 2)
    xc, yc = footprint_center
    out: dict[tuple[int, int, int], tuple[int, int]] = {}
    for (y, x, h) in yxh:
        dx = (paksize / 2) * (x - xc) - (paksize / 2) * (y - yc)
        dy = (paksize / 4) * (x - xc) + (paksize / 4) * (y - yc)
        out[(y, x, h)] = (int(round(dx)),
                          int(round(dy)) - h * paksize)
    return out


def cell_keep_masks(
    cells_yxh,
    *,
    footprint_center: tuple[float, float] | None = None,
    paksize: int = W,
) -> dict[tuple[int, int, int], np.ndarray]:
    """Per-cell keep-masks in sprite frame for the given footprint.  Used
    by `pak.viewpoints` to wire `alpha_mask` per Slice."""
    anchors = cell_anchors(cells_yxh,
                           footprint_center=footprint_center,
                           paksize=paksize)
    return cell_split.cell_keep_masks(anchors, _lattice(paksize))


def stitch(
    cells,
    anchors,
    *,
    into_canvas: np.ndarray | None = None,
    pad: int = 16,
    paksize: int = W,
) -> tuple[np.ndarray, dict[tuple[int, int, int], tuple[int, int]]]:
    """Square wrapper around `pak.cell_split.stitch`."""
    return cell_split.stitch(cells, anchors, _lattice(paksize),
                             into_canvas=into_canvas, pad=pad)


def split(
    canvas: np.ndarray,
    anchors,
    *,
    paksize: int = W,
) -> dict[tuple[int, int, int], np.ndarray]:
    """Square wrapper around `pak.cell_split.split`."""
    return cell_split.split(canvas, anchors, _lattice(paksize))


def claim_mask(
    cells,
    anchors,
    canvas_shape: tuple[int, int],
    *,
    paksize: int = W,
) -> np.ndarray:
    """Square wrapper around `pak.cell_split.claim_mask`."""
    return cell_split.claim_mask(cells, anchors, canvas_shape,
                                 _lattice(paksize))
