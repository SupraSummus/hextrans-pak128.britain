"""Square footprint -> hex footprint mapping.

Axiom: sq tile edge = hex tile edge = `HEX_TILE_RADIUS` (1 world unit).
A `dims_x x dims_y` sq footprint is a 45°-rotated unit-cell rectangle
(the dimetric convention) in the hex world frame; the solver finds
the set of axial hex cells whose flat-top polygons cover it, sweeping
the seven candidate translations in `CANDIDATE_OFFSETS` (hex tile
center plus the three vertex orbits and three edge midpoint orbits
that survive sq's 45° D2 symmetry) and returning the placements with
the fewest cells.
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


def _cube_round(
    xc: np.ndarray, zc: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Vectorised hex cube-coord rounding; returns `(q, r) = (x, z)` as
    int arrays.  Repairs the rounded triple to satisfy `x + y + z = 0`
    by fixing whichever axis took the largest rounding error."""
    yc = -xc - zc
    rxc = np.round(xc)
    ryc = np.round(yc)
    rzc = np.round(zc)
    dx = np.abs(rxc - xc)
    dy = np.abs(ryc - yc)
    dz = np.abs(rzc - zc)
    fix_x = (dx > dy) & (dx > dz)
    fix_y = ~fix_x & (dy > dz)
    fix_z = ~fix_x & ~fix_y
    rxc = np.where(fix_x, -ryc - rzc, rxc)
    ryc = np.where(fix_y, -rxc - rzc, ryc)
    rzc = np.where(fix_z, -rxc - ryc, rzc)
    return rxc.astype(int), rzc.astype(int)


def world_to_axial(x: float, y: float) -> tuple[int, int]:
    """Nearest hex `(q, r)` for world point `(x, y)`."""
    qf = (2.0 / 3.0) * x / HEX_TILE_RADIUS
    rf = (-x / 3.0 + y / _SQRT3) / HEX_TILE_RADIUS
    q, r = _cube_round(np.array([qf]), np.array([rf]))
    return int(q[0]), int(r[0])


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
    samples_per_unit: int = 32,
) -> set[tuple[int, int]]:
    """Hex axial cells containing any sample point of a `dims_x * dims_y`
    rectangle centred at `centroid_world` and rotated by `rotation_deg`."""
    cx, cy = centroid_world
    theta = math.radians(rotation_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    nx = max(2, int(dims_x * samples_per_unit))
    ny = max(2, int(dims_y * samples_per_unit))
    xs = (np.arange(nx) + 0.5) / samples_per_unit - dims_x / 2.0
    ys = (np.arange(ny) + 0.5) / samples_per_unit - dims_y / 2.0
    xx, yy = np.meshgrid(xs, ys)
    wx = (cos_t * xx - sin_t * yy + cx).ravel()
    wy = (sin_t * xx + cos_t * yy + cy).ravel()
    qf = (2.0 / 3.0) * wx / HEX_TILE_RADIUS
    rf = (-wx / 3.0 + wy / _SQRT3) / HEX_TILE_RADIUS
    qs, rs = _cube_round(qf, rf)
    return set(zip(qs.tolist(), rs.tolist()))


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

