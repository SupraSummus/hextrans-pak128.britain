"""Universal square-footprint -> hex-footprint mapping.

For a `dims_x x dims_y` square-dimetric building footprint, returns
the minimal set of hex axial cells whose claim under `pak.hex_split`
covers the sq diamond polygon.  Tries candidate anchor placements
(hex tile center, vertex, edge midpoints) under translation only and
picks the placement with the fewest claimed hex cells; tiebreak is
the axial bounding box (smallest `Dims=` rectangle).

`dims_x = dims_y = 1` is the degenerate case: the sq diamond is W
wide x W/2 tall and the hex polygon contains it, so the algorithm
returns `[(0, 0)]` with the tile-center anchor.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from pak import cell_split
from pak.hex_split import _lattice as _hex_lattice
from pak.hex_split import hex_tile_screen_offset
from pak.sq_split import W

# Anchor offsets within one hex tile, expressed as the screen-pixel
# translation FROM "sq centroid sitting on the hex (0,0) tile center"
# TO the named symmetric point.  All other lattice positions are
# congruent to one of these under axial translation.
#
# Hex polygon corners (from `hex_polygon_bottom_trim`): (+/-W/2, 0)
# left/right vertices, (+/-W/4, +/-W/4) corners.  Three edge orbits:
# top/bottom flat, NE/SW slash, NW/SE backslash.  Two vertex orbits:
# upper vs lower (the up- and down-pointing triangle vertices).
CANDIDATE_ANCHORS: dict[str, tuple[float, float]] = {
    "tile_center":     (0.0, 0.0),
    # Edge midpoint of the (0,0) hex's upper-left edge -- shared with
    # the (-1, 0) tile at (-0.75W, -0.25W).  Midpoint: (-0.375W, -0.125W).
    "edge_backslash":  (-0.375 * W, -0.125 * W),
    # Upper-right edge midpoint, shared with (+1, 0).  (0.375W, -0.125W).
    "edge_slash":      (0.375 * W, -0.125 * W),
    # Top edge midpoint, shared with (0, -1).  (0, -W/4).
    "edge_horizontal": (0.0, -0.25 * W),
    # Upper vertex: meeting of (0,0), (0,-1), (+1,-1) ... actually
    # any vertex orbit; one representative each.
    "vertex_up":       (0.25 * W, -0.25 * W),
    "vertex_down":     (-0.25 * W, +0.25 * W),
}


@dataclass(frozen=True)
class HexFootprint:
    """Result of `sq_to_hex_footprint`.

    `cells` are axial (q, r) keys, normalised so min(q)==min(r)==0.
    `anchor_kind` names the winning symmetric point on the hex lattice.
    `anchor_offset_px` is the screen translation from the sq footprint
    centroid to the hex (0, 0) tile's ground anchor, in pixels.
    `bbox_qr` is `(span_q, span_r)` -- the engine `Dims=` rectangle.
    """
    cells: tuple[tuple[int, int], ...]
    anchor_kind: str
    anchor_offset_px: tuple[int, int]
    bbox_qr: tuple[int, int]

    @property
    def n_cells(self) -> int:
        return len(self.cells)


def sq_diamond_mask(
    dims_x: int, dims_y: int, pad_tiles: int = 4,
) -> tuple[np.ndarray, tuple[int, int]]:
    """Union of sq cell ground polygons (the "diamond polygon") for the
    `dims_x x dims_y` footprint.  Returns `(mask, centroid_xy)` where
    `mask` is a bool array on a canvas large enough to hold the diamond
    plus `pad_tiles` extra hex tiles of slack on every side, and
    `centroid_xy` is the pixel position of the sq footprint centroid in
    that canvas."""
    half = W // 2
    fourth = W // 4
    # Diamond extent in pixels (centred): width (dx+dy)*half, height (dx+dy)*fourth.
    diam_w = (dims_x + dims_y) * half
    diam_h = (dims_x + dims_y) * fourth
    pad = pad_tiles * W
    canvas_w = diam_w + 2 * pad
    canvas_h = diam_h + 2 * pad
    canvas = np.zeros((canvas_h, canvas_w), dtype=bool)
    cx, cy = canvas_w // 2, canvas_h // 2

    # Each cell's ground polygon -- diamond inside the 128² sprite,
    # anchored at (W/2, 3W/4), with corners (+/-W/2, 0), (0, +/-W/4).
    ys_local, xs_local = np.indices((W, W))
    dx_local = xs_local - half
    dy_local = ys_local - (3 * W // 4)
    cell_poly = np.abs(dx_local) + 2 * np.abs(dy_local) <= half

    xc = (dims_x - 1) / 2.0
    yc = (dims_y - 1) / 2.0
    for y in range(dims_y):
        for x in range(dims_x):
            ax = cx + int(round(half * (x - xc) - half * (y - yc)))
            ay = cy + int(round(fourth * (x - xc) + fourth * (y - yc)))
            tlx = ax - half
            tly = ay - 3 * W // 4
            canvas[tly:tly + W, tlx:tlx + W] |= cell_poly
    return canvas, (cx, cy)


def _hex_cells_covering(
    mask: np.ndarray,
    sq_centroid: tuple[int, int],
    anchor_offset: tuple[float, float],
    *,
    radius: int = 6,
) -> tuple[list[tuple[int, int]], np.ndarray, dict]:
    """Run the hex partition over a `(2*radius+1)^2` axial grid around
    the sq footprint and return the axial cells that claim any True
    pixel of `mask`.

    Returns `(claimed_cells, owner_map, anchors)`.  `owner_map[y, x]`
    is the index into the back-first-sorted cell list, -1 if unclaimed;
    `anchors` is the input dict keyed by `(q, r, 0)` carrying each cell's
    ground anchor in canvas pixels (so the viz can draw cell outlines).
    """
    cx, cy = sq_centroid
    hex_ax = cx + int(round(anchor_offset[0]))
    hex_ay = cy + int(round(anchor_offset[1]))
    anchors: dict[tuple[int, int, int], tuple[int, int]] = {}
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            dx, dy = hex_tile_screen_offset(q, r)
            anchors[(q, r, 0)] = (hex_ax + int(round(dx)),
                                  hex_ay + int(round(dy)))
    lattice = _hex_lattice(W)
    owner, cells = cell_split._owner_map(anchors, lattice, mask.shape)
    used_idx = np.unique(owner[mask])
    used_idx = used_idx[used_idx >= 0]
    claimed = [(cells[i][0], cells[i][1]) for i in used_idx]
    return claimed, owner, anchors


def sq_to_hex_footprint(dims_x: int, dims_y: int) -> HexFootprint:
    """Universal sq -> hex footprint solver.  See module docstring."""
    mask, centroid = sq_diamond_mask(dims_x, dims_y)
    best: tuple | None = None
    for kind, offset in CANDIDATE_ANCHORS.items():
        claimed, _owner, _anchors = _hex_cells_covering(mask, centroid, offset)
        qs = [q for q, _ in claimed]
        rs = [r for _, r in claimed]
        span_q = max(qs) - min(qs)
        span_r = max(rs) - min(rs)
        ofs_q, ofs_r = -min(qs), -min(rs)
        norm = tuple(sorted((q + ofs_q, r + ofs_r) for q, r in claimed))
        score = (len(claimed), (span_q + 1) * (span_r + 1), span_q + span_r)
        if best is None or score < best[0]:
            best = (score, kind, offset, norm, (span_q + 1, span_r + 1))
    _score, kind, offset, cells, bbox = best
    return HexFootprint(
        cells=cells,
        anchor_kind=kind,
        anchor_offset_px=(int(round(offset[0])), int(round(offset[1]))),
        bbox_qr=bbox,
    )


if __name__ == "__main__":
    # Quick console dump for inspection.
    for n in (1, 2, 3):
        for m in (1, 2, 3):
            fp = sq_to_hex_footprint(n, m)
            print(f"{n}x{m}: anchor={fp.anchor_kind:<18s} "
                  f"n_cells={fp.n_cells} bbox={fp.bbox_qr} cells={list(fp.cells)}")
