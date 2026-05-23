"""Square dimetric per-tile cutter for multi-tile, multi-height
buildings.  Port of An-dz/tilecutter's `TCMaskSet` + `export_cutter`
(https://github.com/An-dz/tilecutter, file `tc.py`).

Each `(y, x, h)` cell gets a fixed `paksize²` mask chosen by which
corner of the footprint the cell sits at (back-corner / SE back-edge
/ SW back-edge / interior) and whether it's at ground level or
elevated.  No neighbour-distance metric.  See `mask_id` for the
corner-case rules and `_build_masks` for the seven mask compositions.

For pak128 (`paksize=128`): `half=64`, `fourth=32`.  Ground anchor
inside each 128² cell at `(half, half + fourth) = (64, 96)`.
"""

from __future__ import annotations

import numpy as np

W = 128
GROUND_ANCHOR = (64, 96)
MAGIC_PINK = np.array([231, 255, 255], dtype=np.uint8)


def _bottom_triangles(paksize: int = W) -> np.ndarray:
    """Mask out (set True = transparent) the two bottom-corner
    triangles outside the diamond, per TileCutter's
    `fill_bottom_triangles`."""
    half = paksize // 2
    fourth = paksize // 4
    out = np.zeros((paksize, paksize), dtype=bool)
    ys, xs = np.indices((paksize, paksize))
    # Bottom rows half+fourth..paksize-1 (= 96..127 for pak128).
    # Per-row: left triangle x < 2*(y - (half+fourth)) AND right
    # triangle x >= paksize - 2*(y - (half+fourth)).
    dy = ys - (half + fourth)
    bot = dy >= 0
    left = bot & (xs < 2 * dy)
    right = bot & (xs >= paksize - 2 * dy)
    out |= left | right
    return out


def _top_left(paksize: int = W) -> np.ndarray:
    """Mask out the top-left quadrant + a small wedge joining it to
    the diamond's left flank, per TileCutter's `fill_top_left`."""
    half = paksize // 2
    fourth = paksize // 4
    out = np.zeros((paksize, paksize), dtype=bool)
    ys, xs = np.indices((paksize, paksize))
    # Top-left quadrant: rows 0..half (inclusive), cols 0..half-1.
    out |= (ys <= half) & (xs < half)
    # Small wedge above the diamond's left flank: rows half+fourth-y
    # for y in 0..fourth-1, x in 0..2y-1.  Equivalently, in (x, y):
    # rows half+1..half+fourth-1, x < 2*((half+fourth) - y).
    dy_up = (half + fourth) - ys
    wedge_rows = (dy_up >= 1) & (dy_up <= fourth - 1)
    wedge = wedge_rows & (xs < 2 * dy_up)
    out |= wedge
    return out


def _top_right(paksize: int = W) -> np.ndarray:
    """Mirror of `_top_left`."""
    half = paksize // 2
    fourth = paksize // 4
    out = np.zeros((paksize, paksize), dtype=bool)
    ys, xs = np.indices((paksize, paksize))
    out |= (ys <= half) & (xs >= half)
    dy_up = (half + fourth) - ys
    wedge_rows = (dy_up >= 1) & (dy_up <= fourth - 1)
    wedge = wedge_rows & (xs >= paksize - 2 * dy_up)
    out |= wedge
    return out


def _left_half(paksize: int = W) -> np.ndarray:
    out = np.zeros((paksize, paksize), dtype=bool)
    out[:, :paksize // 2] = True
    return out


def _right_half(paksize: int = W) -> np.ndarray:
    out = np.zeros((paksize, paksize), dtype=bool)
    out[:, paksize // 2:] = True
    return out


def _build_masks(paksize: int = W) -> dict[int, np.ndarray]:
    """Return `{mask_id: keep_mask}` for TileCutter's 7 masks; `True`
    in the result means "keep this pixel" (the inverse of TileCutter's
    "fill = mask out")."""
    bt = _bottom_triangles(paksize)
    tl = _top_left(paksize)
    tr = _top_right(paksize)
    lh = _left_half(paksize)
    rh = _right_half(paksize)
    out_out: dict[int, np.ndarray] = {
        0:  ~(bt | tl | tr),    # diamond only
        1:  ~(bt | tl),         # diamond + top-right
        2:  ~(bt | tr),         # diamond + top-left
        3:  ~bt,                # diamond + full top
        4:  ~lh,                # right half
        5:  ~rh,                # left half
        6:  np.ones((paksize, paksize), dtype=bool),  # everything
        -1: np.zeros((paksize, paksize), dtype=bool),  # nothing
    }
    return out_out


_MASKS = _build_masks()


def mask_id(y: int, x: int, h: int) -> int:
    """TileCutter mask id for cell `(y, x, h)` in a rectangular
    footprint where `(0, 0)` is the back corner.

    TileCutter's tc.py uses `(x, y)` with `+x` heading SW in screen
    space (see `tile_to_screen`'s `xx = (xdims-1-xpos+ypos) * p/2`).
    The hex / Simutrans engine convention has `+x` heading SE.  The
    two `(x, y)` axes therefore swap; the rules below already apply
    the swap so that callers can pass engine-frame `(y, x)`
    directly.

    Geometric meaning per case:

      * `(y, x) == (0, 0)` -- the absolute back corner.  Keeps
        diamond + all top (`3` / `6` for `h > 0`).
      * `(y, x) == (0, _)` -- back-row SE edge.  No tile at
        `y < 0`, so this cell keeps its top-RIGHT.  (`1` / `4`)
      * `(y, x) == (_, 0)` -- back-column SW edge.  No tile at
        `x < 0`, so this cell keeps its top-LEFT.  (`2` / `5`)
      * else -- interior / front.  Diamond only (`0`), or empty at
        `h > 0` (`-1`).
    """
    if h == 0:
        if y == 0 and x == 0:
            return 3
        if y == 0:
            return 1
        if x == 0:
            return 2
        return 0
    if y == 0 and x == 0:
        return 6
    if y == 0:
        return 4
    if x == 0:
        return 5
    return -1


def cell_mask(y: int, x: int, h: int, *, paksize: int = W) -> np.ndarray:
    """Boolean `(paksize, paksize)` keep-mask for cell `(y, x, h)`."""
    if paksize == W:
        return _MASKS[mask_id(y, x, h)]
    return _build_masks(paksize)[mask_id(y, x, h)]


def cell_anchors(
    cells_yxh,
    *,
    footprint_center: tuple[float, float] | None = None,
    paksize: int = W,
) -> dict[tuple[int, int, int], tuple[int, int]]:
    """Map each `(y, x, h)` to its ground-anchor in a canvas frame
    whose origin sits at `(0, 0)`.  Caller adds a final shift to
    bring all anchors into a positive-coordinate canvas (see
    `stitch`).  Heights stack at `paksize` px per `h` step, matching
    the engine's `ypos -= raster_width` paint loop in
    `obj/gebaeude.cc::display`."""
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


def _cell_topleft(anchor: tuple[int, int], paksize: int) -> tuple[int, int]:
    """Convert a ground anchor to the cell sprite's top-left in the
    same frame.  `GROUND_ANCHOR` scales with paksize."""
    return (anchor[0] - GROUND_ANCHOR[0] * paksize // W,
            anchor[1] - GROUND_ANCHOR[1] * paksize // W)


def _clipped_window(top_left: tuple[int, int], paksize: int,
                    canvas_h: int, canvas_w: int):
    """Intersect a `paksize²` window at `top_left` with the canvas
    bounds.  Returns `(canvas_slice, cell_slice)` -- two `(ys, xs)`
    slice pairs aligning the same pixels in canvas frame vs cell
    frame -- or `None` if the window is entirely off-canvas."""
    x0, y0 = top_left
    wx0, wy0 = max(0, x0), max(0, y0)
    wx1 = min(canvas_w, x0 + paksize)
    wy1 = min(canvas_h, y0 + paksize)
    if wx1 <= wx0 or wy1 <= wy0:
        return None
    lx0, ly0 = wx0 - x0, wy0 - y0
    lx1, ly1 = lx0 + (wx1 - wx0), ly0 + (wy1 - wy0)
    return (slice(wy0, wy1), slice(wx0, wx1)), (slice(ly0, ly1), slice(lx0, lx1))


def stitch(
    cells: dict[tuple[int, int, int], np.ndarray],
    anchors: dict[tuple[int, int, int], tuple[int, int]],
    *,
    into_canvas: np.ndarray | None = None,
    pad: int = 16,
    paksize: int = W,
) -> tuple[np.ndarray, dict[tuple[int, int, int], tuple[int, int]]]:
    """Paste each cell on a canvas at its anchor; return
    `(canvas, shifted_anchors)`.

    Two framing modes:

      * `into_canvas=None` (default) -- auto-frame a fresh canvas
        sized to fit every cell window with `pad` px slack on each
        side; anchors are shifted to land inside.
      * `into_canvas=<ndarray>` -- paste into the caller's canvas
        without shifting (used by the cut->stitch roundtrip test
        where the canvas frame is fixed by the input).

    Non-PINK pixels overwrite; paste order = sorted-key iteration
    (irrelevant for strict-partition assets).
    """
    if into_canvas is None:
        ax_min = min(_cell_topleft(a, paksize)[0] for a in anchors.values())
        ay_min = min(_cell_topleft(a, paksize)[1] for a in anchors.values())
        ax_max = max(_cell_topleft(a, paksize)[0] for a in anchors.values()) + paksize
        ay_max = max(_cell_topleft(a, paksize)[1] for a in anchors.values()) + paksize
        sx, sy = -ax_min + pad, -ay_min + pad
        cw, ch = ax_max - ax_min + 2 * pad, ay_max - ay_min + 2 * pad
        canvas = np.empty((ch, cw, 4), dtype=np.uint8)
        canvas[..., :3] = MAGIC_PINK
        canvas[..., 3] = 255
    else:
        canvas = into_canvas
        sx, sy = 0, 0
        ch, cw = canvas.shape[:2]

    shifted: dict[tuple[int, int, int], tuple[int, int]] = {}
    for k in sorted(anchors):
        cell = cells[k]
        sax, say = anchors[k][0] + sx, anchors[k][1] + sy
        shifted[k] = (sax, say)
        win = _clipped_window(_cell_topleft((sax, say), paksize),
                              paksize, ch, cw)
        if win is None:
            continue
        cs, ls = win
        non_pink = (cell[ls][..., :3] != MAGIC_PINK).any(axis=-1)
        canvas[cs][non_pink] = cell[ls][non_pink]
    return canvas, shifted


def split(
    canvas: np.ndarray,
    anchors: dict[tuple[int, int, int], tuple[int, int]],
    *,
    paksize: int = W,
) -> dict[tuple[int, int, int], np.ndarray]:
    """Cut `canvas` into per-cell `paksize²` sprites by TileCutter
    mask.  Returns `{(y, x, h): ndarray((paksize, paksize, 4),
    uint8)}` -- each cell PINK-filled where its mask masks out, the
    canvas content where its mask keeps."""
    masks = _MASKS if paksize == W else _build_masks(paksize)
    ch, cw = canvas.shape[:2]
    out: dict[tuple[int, int, int], np.ndarray] = {}
    for k, anchor in anchors.items():
        keep = masks[mask_id(*k)]
        cell = np.empty((paksize, paksize, 4), dtype=np.uint8)
        cell[..., :3] = MAGIC_PINK
        cell[..., 3] = 255
        win = _clipped_window(_cell_topleft(anchor, paksize),
                              paksize, ch, cw)
        if win is not None:
            cs, ls = win
            keep_win = keep[ls]
            cell[ls][keep_win] = canvas[cs][keep_win]
        out[k] = cell
    return out


def claim_mask(
    cells: dict[tuple[int, int, int], np.ndarray],
    anchors: dict[tuple[int, int, int], tuple[int, int]],
    canvas_shape: tuple[int, int],
    *,
    paksize: int = W,
) -> np.ndarray:
    """Per-pixel claim count: how many cells' non-PINK content lands
    at each canvas pixel.  `> 1` anywhere == partition not disjoint;
    `== 0` on a content pixel == loss.  Used by the property tests."""
    ch, cw = canvas_shape[:2]
    count = np.zeros((ch, cw), dtype=np.int32)
    for k, cell in cells.items():
        win = _clipped_window(_cell_topleft(anchors[k], paksize),
                              paksize, ch, cw)
        if win is None:
            continue
        cs, ls = win
        non_pink = (cell[ls][..., :3] != MAGIC_PINK).any(axis=-1)
        count[cs] += non_pink.astype(np.int32)
    return count
