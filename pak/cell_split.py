"""Projection-agnostic cell-split driver.

Algorithm: each canvas pixel is owned by the most-BACK cell whose
`box x box` sprite covers it.  Ground-level cells additionally get the
bottom-corner region outside the polygon (diamond / hex / ...) pre-trimmed
out of their footprint, so those pixels stay unclaimed.

Equivalent pixel-exact to An-dz/tilecutter's 7 fixed masks under the
square dimetric projection (verified on OilRefinery1955) -- the closed-
form mask lookup is what the back-wins iteration computes when the
projection is dimetric.  Generalizes to any projection by swapping the
bottom-trim mask + paint-key + lattice geometry.

Implementation: iterate cells in back-first paint order on a canvas-sized
owner map, each cell claiming pixels in its sprite footprint MINUS already-
claimed.  Per-cell keep-masks fall out of the owner map.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np

MAGIC_PINK = np.array([231, 255, 255], dtype=np.uint8)


@dataclass(frozen=True)
class Lattice:
    """Per-projection data the cutter consumes.

    `box`: per-cell sprite size in pixels (square pak: 128).
    `ground_anchor`: `(x, y)` of the cell's ground anchor inside the
    `box x box` sprite.  Both square dimetric and hex share `(box/2,
    3*box/4)`.
    `bottom_trim`: `(box, box)` bool mask; True pixels are trimmed from
    every ground-level cell's footprint (the bottom-corner region outside
    the polygon).
    `paint_key`: maps a cell key to a sortable tuple; smallest = most BACK
    = claims canvas pixels first.
    `is_ground`: returns True for cells that get bottom-trimmed (typically
    `h == 0`).
    """
    box: int
    ground_anchor: tuple[int, int]
    bottom_trim: np.ndarray
    paint_key: Callable[[Any], tuple]
    is_ground: Callable[[Any], bool]

    def box_topleft(self, anchor: tuple[int, int]) -> tuple[int, int]:
        return (anchor[0] - self.ground_anchor[0],
                anchor[1] - self.ground_anchor[1])


def _clipped_window(top_left: tuple[int, int], box: int,
                    canvas_h: int, canvas_w: int):
    """Intersect a `box x box` window at `top_left` with the canvas bounds.
    Returns `(canvas_slice, cell_slice)` or `None` if entirely off-canvas."""
    x0, y0 = top_left
    wx0, wy0 = max(0, x0), max(0, y0)
    wx1 = min(canvas_w, x0 + box)
    wy1 = min(canvas_h, y0 + box)
    if wx1 <= wx0 or wy1 <= wy0:
        return None
    lx0, ly0 = wx0 - x0, wy0 - y0
    lx1, ly1 = lx0 + (wx1 - wx0), ly0 + (wy1 - wy0)
    return (slice(wy0, wy1), slice(wx0, wx1)), (slice(ly0, ly1), slice(lx0, lx1))


def _owner_map(anchors: dict, lattice: Lattice,
               canvas_shape: tuple[int, int]) -> tuple[np.ndarray, list]:
    """Build the canvas-frame ownership map.  Returns `(owner, cells)`
    where `cells` is the back-first paint order and `owner[y, x]` is the
    index into `cells` (or -1 if unclaimed)."""
    ch, cw = canvas_shape
    box = lattice.box
    cells = sorted(anchors, key=lattice.paint_key)
    owner = np.full((ch, cw), -1, dtype=np.int32)
    for idx, k in enumerate(cells):
        win = _clipped_window(lattice.box_topleft(anchors[k]), box, ch, cw)
        if win is None:
            continue
        cs, ls = win
        region = owner[cs]
        keep = region == -1
        if lattice.is_ground(k):
            keep &= ~lattice.bottom_trim[ls]
        region[keep] = idx
    return owner, cells


def _auto_frame(anchors: dict, lattice: Lattice, *, pad: int = 0):
    """Tight `(canvas_shape, (shift_x, shift_y))` to fit every cell sprite
    with `pad` px slack on each side.  Shared by `cell_keep_masks` (no
    pad) and `stitch`'s auto-frame branch."""
    topleft = [lattice.box_topleft(a) for a in anchors.values()]
    min_x = min(t[0] for t in topleft) - pad
    min_y = min(t[1] for t in topleft) - pad
    max_x = max(t[0] for t in topleft) + lattice.box + pad
    max_y = max(t[1] for t in topleft) + lattice.box + pad
    return (max_y - min_y, max_x - min_x), (-min_x, -min_y)


def cell_keep_masks(anchors: dict, lattice: Lattice) -> dict:
    """Per-cell keep-masks in sprite frame: `{cell_key: (box, box) bool}`.

    Auto-sizes a virtual canvas tight to the anchor extents; the masks
    themselves are projection-frame-independent (they describe each cell's
    claim within its own `box x box` sprite).  Used by viewpoints to wire
    per-cell `alpha_mask` for the compose step."""
    box = lattice.box
    canvas_shape, (sx, sy) = _auto_frame(anchors, lattice)
    shifted = {k: (a[0] + sx, a[1] + sy) for k, a in anchors.items()}
    owner, cells = _owner_map(shifted, lattice, canvas_shape)
    out: dict = {}
    for idx, k in enumerate(cells):
        tl = lattice.box_topleft(shifted[k])
        out[k] = owner[tl[1]:tl[1] + box, tl[0]:tl[0] + box] == idx
    return out


def split(canvas: np.ndarray, anchors: dict, lattice: Lattice) -> dict:
    """Cut `canvas` into per-cell `(box, box, 4) uint8` sprites.

    Each cell sprite is MAGIC_PINK where the cell doesn't own the canvas
    pixel and copies the canvas content where it does."""
    box = lattice.box
    ch, cw = canvas.shape[:2]
    owner, cells = _owner_map(anchors, lattice, (ch, cw))
    out: dict = {}
    for idx, k in enumerate(cells):
        sprite = np.empty((box, box, 4), dtype=np.uint8)
        sprite[..., :3] = MAGIC_PINK
        sprite[..., 3] = 255
        win = _clipped_window(lattice.box_topleft(anchors[k]), box, ch, cw)
        if win is not None:
            cs, ls = win
            mine = owner[cs] == idx
            sprite[ls][mine] = canvas[cs][mine]
        out[k] = sprite
    return out


def stitch(
    cells: dict,
    anchors: dict,
    lattice: Lattice,
    *,
    into_canvas: np.ndarray | None = None,
    pad: int = 16,
) -> tuple[np.ndarray, dict]:
    """Paste each cell on a canvas at its anchor; return
    `(canvas, shifted_anchors)`.

    Cell sprites from `split` are pixel-disjoint by construction, so paste
    order doesn't matter -- MAGIC_PINK pixels are skipped, non-PINK overwrite.
    Auto-frames a fresh canvas if `into_canvas is None`, otherwise pastes
    into the caller's canvas without shifting (used by the cut->stitch
    roundtrip).
    """
    box = lattice.box
    if into_canvas is None:
        (ch, cw), (sx, sy) = _auto_frame(anchors, lattice, pad=pad)
        canvas = np.empty((ch, cw, 4), dtype=np.uint8)
        canvas[..., :3] = MAGIC_PINK
        canvas[..., 3] = 255
    else:
        canvas = into_canvas
        sx, sy = 0, 0
        ch, cw = canvas.shape[:2]

    shifted: dict = {}
    for k in sorted(anchors):
        cell = cells[k]
        sax, say = anchors[k][0] + sx, anchors[k][1] + sy
        shifted[k] = (sax, say)
        win = _clipped_window(lattice.box_topleft((sax, say)), box, ch, cw)
        if win is None:
            continue
        cs, ls = win
        non_pink = (cell[ls][..., :3] != MAGIC_PINK).any(axis=-1)
        canvas[cs][non_pink] = cell[ls][non_pink]
    return canvas, shifted


def claim_mask(
    cells: dict,
    anchors: dict,
    canvas_shape: tuple[int, int],
    lattice: Lattice,
) -> np.ndarray:
    """Per-pixel claim count.  The partition is strict so `claim_mask <= 1`
    always; kept for the existing property tests."""
    ch, cw = canvas_shape[:2]
    count = np.zeros((ch, cw), dtype=np.int32)
    for k, cell in cells.items():
        win = _clipped_window(lattice.box_topleft(anchors[k]),
                              lattice.box, ch, cw)
        if win is None:
            continue
        cs, ls = win
        non_pink = (cell[ls][..., :3] != MAGIC_PINK).any(axis=-1)
        count[cs] += non_pink.astype(np.int32)
    return count
