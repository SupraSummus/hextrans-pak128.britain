"""Square footprint -> hex footprint mapping.

Axiom: sq tile edge = hex tile edge = `HEX_TILE_RADIUS` (1 world unit).
A `dims_x x dims_y` sq footprint is a 45°-rotated unit-cell rectangle
(the dimetric convention) in the hex world frame; the solver finds,
via exact Separating-Axis-Theorem polygon overlap, the set of axial
hex cells whose flat-top polygons cover it, sweeping the seven
candidate translations in `CANDIDATE_OFFSETS` (hex tile center plus
the three vertex orbits and three edge midpoint orbits that survive
sq's 45° D2 symmetry) and returning the placements with the fewest
cells.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from pak.way import HEX_TILE_RADIUS

_SQRT3 = math.sqrt(3.0)


def hex_world_center(q: int, r: int) -> tuple[float, float]:
    """Flat-top hex `(q, r)` center in world coords.  `+q` steps to the
    right-and-slightly-up; `+r` steps straight up."""
    return (1.5 * HEX_TILE_RADIUS * q,
            _SQRT3 * HEX_TILE_RADIUS * (r + q / 2.0))


def _convex_polys_overlap(a: np.ndarray, b: np.ndarray) -> bool:
    """Separating-axis-theorem test for two convex polygons.  Returns
    True iff their intersection has positive area; tangent contact
    (shared vertex or edge, zero-area overlap) returns False."""
    for poly in (a, b):
        n = len(poly)
        for i in range(n):
            edge = poly[(i + 1) % n] - poly[i]
            axis = np.array([-edge[1], edge[0]])
            ap = a @ axis
            bp = b @ axis
            if ap.max() <= bp.min() or bp.max() <= ap.min():
                return False
    return True


# Sq centroid placements modulo hex lattice + sq's 45° D2 symmetry: hex
# tile center, three vertex orbits (one per sq-axis direction), three
# edge-midpoint orbits.
_R = HEX_TILE_RADIUS
_H = _SQRT3 / 2.0 * HEX_TILE_RADIUS
CANDIDATE_OFFSETS: dict[str, tuple[float, float]] = {
    "tile_center":       (0.0, 0.0),
    "vertex_horizontal": (_R, 0.0),
    "vertex_slash":      (0.5 * _R, _H),
    "vertex_backslash":  (-0.5 * _R, _H),
    "edge_horizontal":   (0.0, _H),
    "edge_slash":        (0.75 * _R, 0.5 * _H),
    "edge_backslash":    (0.75 * _R, -0.5 * _H),
}

# Flat-top regular hex of edge `HEX_TILE_RADIUS` centred at origin.
_HEX_CORNERS_LOCAL = np.array([
    (_R, 0.0),
    (0.5 * _R, _H),
    (-0.5 * _R, _H),
    (-_R, 0.0),
    (-0.5 * _R, -_H),
    (0.5 * _R, -_H),
])

# Dimetric sq frame is rotated 45° relative to the hex world frame; this
# is the porting axiom, not a free parameter.
SQ_ROTATION_DEG: float = 45.0


@dataclass(frozen=True)
class HexFootprint:
    """Result of `sq_to_hex_footprint`.  `cells` are axial `(q, r)` keys
    normalised so `min(q) == min(r) == 0`; `bbox_qr` is the engine
    `Dims=` rectangle; `anchor_kind` names the hex symmetric point the
    sq centroid sits on (see `CANDIDATE_OFFSETS`)."""
    cells: tuple[tuple[int, int], ...]
    anchor_kind: str
    bbox_qr: tuple[int, int]

    @property
    def n_cells(self) -> int:
        return len(self.cells)


def hex_cells_overlapping_rect(
    dims_x: float, dims_y: float,
    centroid_world: tuple[float, float],
    *,
    rotation_deg: float = SQ_ROTATION_DEG,
) -> set[tuple[int, int]]:
    """Hex axial cells whose flat-top polygon has positive-area
    intersection with the `dims_x * dims_y` rectangle centred at
    `centroid_world` and rotated by `rotation_deg`.

    Exact via Separating-Axis Theorem on the rect and each candidate
    hex polygon -- no sampling, so corner-poke slivers don't escape."""
    cx, cy = centroid_world
    th = math.radians(rotation_deg)
    cos_t, sin_t = math.cos(th), math.sin(th)
    hw, hh = dims_x / 2.0, dims_y / 2.0
    rect_local = np.array([(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)])
    rect = np.column_stack([
        cos_t * rect_local[:, 0] - sin_t * rect_local[:, 1] + cx,
        sin_t * rect_local[:, 0] + cos_t * rect_local[:, 1] + cy,
    ])
    x_min, y_min = rect.min(axis=0) - _R
    x_max, y_max = rect.max(axis=0) + _R
    q_lo = math.floor(x_min / 1.5)
    q_hi = math.ceil(x_max / 1.5)
    cells: set[tuple[int, int]] = set()
    for q in range(q_lo, q_hi + 1):
        r_lo = math.floor(y_min / _SQRT3 - q / 2.0)
        r_hi = math.ceil(y_max / _SQRT3 - q / 2.0)
        for r in range(r_lo, r_hi + 1):
            hcx, hcy = hex_world_center(q, r)
            hex_poly = _HEX_CORNERS_LOCAL + (hcx, hcy)
            if _convex_polys_overlap(rect, hex_poly):
                cells.add((q, r))
    return cells


def _candidate_footprint(dims_x: int, dims_y: int,
                         anchor_kind: str) -> HexFootprint:
    cells = hex_cells_overlapping_rect(
        dims_x, dims_y, CANDIDATE_OFFSETS[anchor_kind])
    qs = [q for q, _ in cells]
    rs = [r for _, r in cells]
    q0, r0 = min(qs), min(rs)
    span_q, span_r = max(qs) - q0, max(rs) - r0
    norm = tuple(sorted((q - q0, r - r0) for q, r in cells))
    return HexFootprint(cells=norm, anchor_kind=anchor_kind,
                        bbox_qr=(span_q + 1, span_r + 1))


def sq_to_hex_all_minimal(dims_x: int, dims_y: int) -> list[HexFootprint]:
    """Every anchor placement that ties for the minimum cell count, in
    `CANDIDATE_OFFSETS` declaration order."""
    cands = [_candidate_footprint(dims_x, dims_y, k)
             for k in CANDIDATE_OFFSETS]
    best_n = min(c.n_cells for c in cands)
    return [c for c in cands if c.n_cells == best_n]


def sq_to_hex_footprint(dims_x: int, dims_y: int) -> HexFootprint:
    """Single representative placement: fewest cells, tiebreak smallest
    `Dims=` rectangle.  See `sq_to_hex_all_minimal` for ties."""
    return min(
        sq_to_hex_all_minimal(dims_x, dims_y),
        key=lambda f: f.bbox_qr[0] * f.bbox_qr[1],
    )


if __name__ == "__main__":
    for n in (1, 2, 3, 4):
        for m in (1, 2, 3, 4):
            fp = sq_to_hex_footprint(n, m)
            print(f"{n}x{m}: anchor={fp.anchor_kind:<16s} "
                  f"n={fp.n_cells} bbox={fp.bbox_qr} "
                  f"cells={list(fp.cells)}")

