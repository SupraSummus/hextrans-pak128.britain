"""Universal square-footprint -> hex-footprint mapping (world coords).

Axiom: square tile edge length = hex tile edge length = 1 world unit.
Both share a world coordinate frame.  A `dims_x x dims_y` sq footprint
spans a world rectangle of area `dims_x * dims_y`; hex tiles are
regular hexagons of edge 1 (circumradius 1, area `3·sqrt(3)/2 ≈ 2.598`),
tiled in flat-top honeycomb.

Goal: find the set of axial-indexed hex tiles whose union of polygons
covers the sq rectangle.  Search over translation offsets between the
sq centroid and the hex lattice (and over rotations of the sq footprint
relative to the hex axes); pick the placement with fewest hex tiles,
tiebreaking by smaller axial bounding box (the engine `Dims=` budget).

`dims_x = dims_y = 1` is the degenerate case: the 1x1 world square has
half-diagonal `sqrt(2)/2 ≈ 0.707`, which fits inside a hex tile's
inscribed circle of radius `sqrt(3)/2 ≈ 0.866`.  So the algorithm
returns one cell `(0, 0)` at tile-center anchor.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

SQRT3 = math.sqrt(3.0)
HEX_EDGE = 1.0  # axiom: hex entry-edge = sq tile side = 1 world unit


def hex_world_center(q: int, r: int) -> tuple[float, float]:
    """Flat-top hex `(q, r)` center in world coords.  Axial basis:
    q-step is `(1.5, sqrt(3)/2)`, r-step is `(0, sqrt(3))`.  This matches
    the projection in `pak.hex_split.hex_tile_screen_offset` (with the
    `y/sqrt(3)` shear and `W/(2R)` scale stripped)."""
    return (1.5 * HEX_EDGE * q,
            SQRT3 * HEX_EDGE * (r + q / 2.0))


def _point_in_hex(px: float, py: float,
                  cx: float = 0.0, cy: float = 0.0) -> bool:
    """True iff `(px, py)` is inside the flat-top regular hex of edge
    `HEX_EDGE` centred at `(cx, cy)`.  Closed boundary; ties broken at
    the call site if needed."""
    dx = abs(px - cx)
    dy = abs(py - cy)
    if dy > SQRT3 / 2.0 * HEX_EDGE + 1e-12:
        return False
    if dx + dy / SQRT3 > HEX_EDGE + 1e-12:
        return False
    return True


def world_to_axial(x: float, y: float) -> tuple[int, int]:
    """Nearest hex `(q, r)` for world point `(x, y)`; cube-coord rounding."""
    qf = (2.0 / 3.0) * x / HEX_EDGE
    rf = (-x / 3.0 + y / SQRT3) / HEX_EDGE
    xc, zc = qf, rf
    yc = -xc - zc
    rxc, ryc, rzc = round(xc), round(yc), round(zc)
    dx, dy, dz = abs(rxc - xc), abs(ryc - yc), abs(rzc - zc)
    if dx > dy and dx > dz:
        rxc = -ryc - rzc
    elif dy > dz:
        ryc = -rxc - rzc
    else:
        rzc = -rxc - ryc
    return int(rxc), int(rzc)


# Candidate placements of the sq footprint centroid relative to the hex
# (0, 0) tile.  Within one fundamental domain (one hex tile), distinct
# symmetric points up to the sq footprint's own symmetry are: hex tile
# center, two vertex orbits (upper / lower), three edge-midpoint orbits
# (the three flat-top edge orientations).  Sq's own 2-fold rotational
# + two reflection symmetries collapse other points to these.
CANDIDATE_OFFSETS: dict[str, tuple[float, float]] = {
    "tile_center":     (0.0, 0.0),
    "vertex_right":    (HEX_EDGE, 0.0),
    "vertex_upper":    (0.5 * HEX_EDGE, SQRT3 / 2.0 * HEX_EDGE),
    "edge_horizontal": (0.0, SQRT3 / 2.0 * HEX_EDGE),
    "edge_slash":      (0.75 * HEX_EDGE, SQRT3 / 4.0 * HEX_EDGE),
    "edge_backslash":  (0.75 * HEX_EDGE, -SQRT3 / 4.0 * HEX_EDGE),
}


# Sq footprint rotation relative to the hex world axes.  Fixed at 45° --
# the dimetric sq frame is rotated 45° relative to the hex world frame,
# so a sq tile is a diamond in the hex world frame; this orientation is
# the porting axiom, not a free parameter.
SQ_ROTATION_DEG: float = 45.0


@dataclass(frozen=True)
class HexFootprint:
    """Result of `sq_to_hex_footprint`.

    `cells` are axial `(q, r)` keys normalised so `min(q) == min(r) == 0`.
    `anchor_kind` names the winning hex-lattice symmetric point the sq
    centroid was placed on.  Sq footprint is fixed at `SQ_ROTATION_DEG`
    (45°) relative to the hex axes -- not a free parameter, see module
    constant.  `bbox_qr` is `(span_q, span_r)` -- the engine `Dims=`
    rectangle.
    """
    cells: tuple[tuple[int, int], ...]
    anchor_kind: str
    bbox_qr: tuple[int, int]

    @property
    def n_cells(self) -> int:
        return len(self.cells)


def _hex_cells_overlapping_rect(
    dims_x: float, dims_y: float,
    centroid_world: tuple[float, float],
    rotation_deg: float = 0.0,
    *,
    samples_per_unit: int = 32,
) -> set[tuple[int, int]]:
    """Rasterise the (rotated) sq rectangle at `samples_per_unit` per
    world unit, returning every hex axial cell that contains at least
    one sample point.

    The rectangle is `dims_x * dims_y` centred at the origin in the sq
    frame; we rotate by `rotation_deg` and translate by
    `centroid_world` into the hex frame."""
    import numpy as np
    cx, cy = centroid_world
    theta = math.radians(rotation_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)

    nx = max(2, int(dims_x * samples_per_unit))
    ny = max(2, int(dims_y * samples_per_unit))
    xs = (np.arange(nx) + 0.5) / samples_per_unit - dims_x / 2.0
    ys = (np.arange(ny) + 0.5) / samples_per_unit - dims_y / 2.0
    Xs, Ys = np.meshgrid(xs, ys)
    # Rotate + translate sq sample points into world hex frame.
    Wx = cos_t * Xs - sin_t * Ys + cx
    Wy = sin_t * Xs + cos_t * Ys + cy

    cells: set[tuple[int, int]] = set()
    for x, y in zip(Wx.ravel(), Wy.ravel()):
        cells.add(world_to_axial(float(x), float(y)))
    return cells


def sq_to_hex_footprint(dims_x: int, dims_y: int) -> HexFootprint:
    """Universal sq -> hex footprint solver in world coords.  See module
    docstring."""
    best: tuple | None = None
    for kind, offset in CANDIDATE_OFFSETS.items():
        cells = _hex_cells_overlapping_rect(
            dims_x, dims_y, offset, rotation_deg=SQ_ROTATION_DEG)
        qs = [q for q, _ in cells]
        rs = [r for _, r in cells]
        span_q = max(qs) - min(qs)
        span_r = max(rs) - min(rs)
        ofs_q, ofs_r = -min(qs), -min(rs)
        norm = tuple(sorted((q + ofs_q, r + ofs_r) for q, r in cells))
        score = (len(cells), (span_q + 1) * (span_r + 1),
                 span_q + span_r)
        if best is None or score < best[0]:
            best = (score, kind, norm, (span_q + 1, span_r + 1))
    _score, kind, cells, bbox = best
    return HexFootprint(cells=cells, anchor_kind=kind, bbox_qr=bbox)


if __name__ == "__main__":
    for n in (1, 2, 3, 4):
        for m in (1, 2, 3, 4):
            fp = sq_to_hex_footprint(n, m)
            print(f"{n}x{m}: anchor={fp.anchor_kind:<16s} "
                  f"n={fp.n_cells} bbox={fp.bbox_qr} "
                  f"cells={list(fp.cells)}")
