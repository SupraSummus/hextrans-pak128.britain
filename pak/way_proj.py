"""Way-bake projection records used by `pak/bake_way.py --projection`.

The composition pipeline (clone atom → place on chord → bisect at
cap planes + tile-outline planes → render) accepts a `Projection`
that bundles the projection-specific knobs: tile geometry (edges,
edge midpoints, edge unit dirs, clip planes), path topology dispatch
(`for_edges_paths(edges)`), camera + sun pose, projection extrinsic,
ortho_scale, and atlas layout.

**Scope today**: hex is production, square is sketched so the diff
harness (TODO.md → "Way square-projection diff harness") has
something to call.  The square path-topology helpers
(`_square_*` below) are deliberately duplicated from
`pak/way_topology.py` rather than consolidated through a shared
tile-geom parameter — the two projections haven't yet been bent by
a real second consumer (the diff harness), so the right
abstraction shape isn't known.  Consolidate once the diff lands
and reveals which accessors are actually load-bearing.  See
CLAUDE.md → "Way-bake architecture" for the design contract.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Optional

from .hex_synth import (
    HEX_TILE_RADIUS, INTRA_TILE_PER_BLEND_UNIT, UPSTREAM_ORTHO_SCALE,
    hex_proj_shear,
)
from .way import (
    HEX_ENTRIES,
    edge_midpoint as hex_edge_midpoint,
    edge_unit_dir as hex_edge_unit_dir,
    hex_clip_planes,
)
from .way_topology import StraightPath, for_edges_paths as hex_for_edges_paths


# ---- Square tile geometry -------------------------------------------------
#
# Square projection is the **upstream-coord calibration view** for the
# (still open) diff harness — see CLAUDE.md → "Way-bake architecture".
# Unlike `HEX_PROJECTION`, which operates in **intra-tile coords**
# (tile edge = 1), `SQUARE_PROJECTION` operates in **blend coords**
# (the upstream-Britain authoring frame, ruler `UPSTREAM_ORTHO_SCALE`)
# so its renders can be pixel-compared against pak128.Britain's
# published cells without a coord conversion in the middle.
#
# The tile half-side is therefore half the upstream camera frame —
# placing the tile diamond inside the rendered image at the same
# size pak128.Britain's authored cells display.  Don't compare this
# value against `HEX_TILE_RADIUS` directly: they live in different
# coord systems.

SQUARE_TILE_HALF: float = UPSTREAM_ORTHO_SCALE / 2.0


# Corner labels follow the same NSEW direction-of-corner convention
# as the hex tile: NE = north-east corner = (+x, +y) quadrant.
SQUARE_CORNERS: dict[str, tuple[float, float]] = {
    "NE": ( SQUARE_TILE_HALF,  SQUARE_TILE_HALF),
    "SE": ( SQUARE_TILE_HALF, -SQUARE_TILE_HALF),
    "SW": (-SQUARE_TILE_HALF, -SQUARE_TILE_HALF),
    "NW": (-SQUARE_TILE_HALF,  SQUARE_TILE_HALF),
}

# Edge → (corner_a, corner_b).  Same orientation convention as
# HEX_EDGES so `edge_unit_dir` derives consistently across projections.
SQUARE_EDGES: dict[str, tuple[str, str]] = {
    "N": ("NE", "NW"),
    "E": ("SE", "NE"),
    "S": ("SW", "SE"),
    "W": ("NW", "SW"),
}

# Opposite-edge pairs — used by the slope/topology callers (`NS` vs
# `EW` straight chords).
SQUARE_OPPOSITE_EDGE: dict[str, str] = {
    "N": "S", "S": "N",
    "E": "W", "W": "E",
}


def square_edge_midpoint(edge: str) -> tuple[float, float]:
    a, b = SQUARE_EDGES[edge]
    ax, ay = SQUARE_CORNERS[a]
    bx, by = SQUARE_CORNERS[b]
    return ((ax + bx) / 2.0, (ay + by) / 2.0)


def square_edge_unit_dir(edge: str) -> tuple[float, float]:
    a, b = SQUARE_EDGES[edge]
    ax, ay = SQUARE_CORNERS[a]
    bx, by = SQUARE_CORNERS[b]
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy)
    return (dx / n, dy / n)


def square_shared_corner(edge_a: str, edge_b: str) -> str:
    """Corner shared by two 90°-adjacent square edges, or `KeyError` if
    the edges don't share a corner (opposite pair)."""
    shared = set(SQUARE_EDGES[edge_a]) & set(SQUARE_EDGES[edge_b])
    assert len(shared) == 1, (
        f"edges {edge_a}/{edge_b} don't share exactly one corner")
    return next(iter(shared))


def square_clip_planes() -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """The four (co, normal) pairs that fence the square tile outline,
    in world XY, normals inward.  Same `clear_inner=True` bisect
    convention as `hex_clip_planes`."""
    out = []
    for edge in SQUARE_EDGES:
        mx, my = square_edge_midpoint(edge)
        n = math.hypot(mx, my)
        out.append(((mx, my), (-mx / n, -my / n)))
    return out


# ---- Square ribi vocabulary -----------------------------------------------
#
# pak128.Britain `way_writer.cc` keys ribis as `N`, `S`, `E`, `W`,
# `NS`, `EW`, `NE`, `NW`, `SE`, `SW`, `NSE`, `NSW`, `NEW`, `SEW`,
# `NSEW`.  Bit positions don't matter for keying (just labels), but a
# popcount-then-clockwise order keeps the atlas row-cluster reading
# nicely.

_SQUARE_BITS: list[str] = ["N", "S", "E", "W"]


def _square_label_for(edges: tuple[str, ...]) -> str:
    """Canonical dat-key label: NSEW concatenation (opposite axes
    paired first), matching upstream's `Image[NS]`, `Image[EW]`,
    `Image[NSE]`, `Image[NSEW]` keys."""
    order = {"N": 0, "S": 1, "E": 2, "W": 3}
    return "".join(sorted(edges, key=order.get))


def _square_entries() -> list[tuple[str, tuple[str, ...]]]:
    entries: list[tuple[str, tuple[str, ...]]] = []
    for popcount in range(1, len(_SQUARE_BITS) + 1):
        for mask in range(1 << len(_SQUARE_BITS)):
            if bin(mask).count("1") != popcount:
                continue
            edges = tuple(name for b, name in enumerate(_SQUARE_BITS) if mask & (1 << b))
            entries.append((_square_label_for(edges), edges))
    return entries


SQUARE_ENTRIES: list[tuple[str, tuple[str, ...]]] = _square_entries()


# ---- Square path topology -------------------------------------------------
#
# Reuses the same `StraightPath` data class as hex.  The 90° bend is
# **approximated as a V-bend** (two-leg chord through the shared
# corner's half-radial), exactly like the 60° hex bend, even though
# upstream pak128 typically authors curved meshes there.  Trading a
# topology-faithful curve for the V-bend is consistent with the
# hex side's choice (CLAUDE.md → "Way-bake architecture": "All
# topology resolves to straight chord pieces"); the calibration diff
# will tell us how badly the V-bend approximation reads under the
# square camera.


def _square_between_edges(edge_a: str, edge_b: str) -> list[StraightPath]:
    return [StraightPath(
        start=square_edge_midpoint(edge_a),
        end=square_edge_midpoint(edge_b),
        cap_a=square_edge_unit_dir(edge_a),
        cap_b=square_edge_unit_dir(edge_b),
    )]


def _square_bend(edge_a: str, edge_b: str) -> list[StraightPath]:
    corner = square_shared_corner(edge_a, edge_b)
    cx, cy = SQUARE_CORNERS[corner]
    # Apex sits halfway between origin and the corner, on the radial.
    norm = math.hypot(cx, cy)
    apex_cap = (cx / norm, cy / norm)
    apex = (cx / 2.0, cy / 2.0)
    return [
        StraightPath(start=square_edge_midpoint(edge_a), end=apex,
                     cap_a=square_edge_unit_dir(edge_a), cap_b=apex_cap,
                     skip_cap_b=True),
        StraightPath(start=apex, end=square_edge_midpoint(edge_b),
                     cap_a=apex_cap, cap_b=square_edge_unit_dir(edge_b),
                     skip_cap_a=True),
    ]


def _square_curve(edge_a: str, edge_b: str) -> list[StraightPath]:
    if set(SQUARE_EDGES[edge_a]) & set(SQUARE_EDGES[edge_b]):
        return _square_bend(edge_a, edge_b)
    return _square_between_edges(edge_a, edge_b)


def _square_stub(edge: str) -> list[StraightPath]:
    end = square_edge_midpoint(edge)
    n = math.hypot(end[0], end[1])
    cap_centre = (-end[1] / n, end[0] / n)
    # Reuse the hex stub fraction so both projections share the
    # "stub stops well short of the centre" visual convention.
    from .way_topology import STUB_LENGTH_FRACTION
    start = (end[0] * (1.0 - STUB_LENGTH_FRACTION),
             end[1] * (1.0 - STUB_LENGTH_FRACTION))
    return [StraightPath(start=start, end=end,
                         cap_a=cap_centre, cap_b=square_edge_unit_dir(edge))]


def square_for_edges_paths(edges: tuple[str, ...]) -> list[StraightPath]:
    if len(edges) == 1:
        return _square_stub(edges[0])
    if len(edges) == 2:
        return _square_curve(edges[0], edges[1])
    return [p
            for i, a in enumerate(edges)
            for b in edges[i + 1:]
            for p in _square_curve(a, b)]


# ---- Projection records ---------------------------------------------------


@dataclass(frozen=True)
class Projection:
    """The projection-shaped knobs `pak/bake_way.py` parameterises over.

    Three groupings (geometry / topology / render-config) packaged so
    one `--projection` flag in the bake driver switches every
    projection-specific constant at once.
    """
    name: str
    entries: list[tuple[str, tuple[str, ...]]]
    edge_midpoint: Callable[[str], tuple[float, float]]
    edge_unit_dir: Callable[[str], tuple[float, float]]
    clip_planes: Callable[[], list[tuple[tuple[float, float], tuple[float, float]]]]
    for_edges_paths: Callable[[tuple[str, ...]], list[StraightPath]]
    ortho_scale: float
    # Camera + sun pose (Euler radians) and location for the bake's
    # single rendered facing.  Both projections render one image per
    # ribi; only the camera/sun setup differs.
    camera_location: tuple[float, float, float]
    camera_rotation_euler: tuple[float, float, float]
    sun_rotation_euler: tuple[float, float, float]
    # Projection extrinsic baked into every clone's mesh data after
    # caps + outline clip.  `None` for square (the camera does the
    # projection); a 4x4 row-major tuple for hex (`hex_proj_shear()`).
    extrinsic: Optional[tuple]
    # Uniform scale factor applied to every atom mesh before
    # composition, or `None` to keep the blend's native scale.  Hex
    # uses `INTRA_TILE_PER_BLEND_UNIT` (= 1/12) to convert from blend
    # coords into the intra-tile coord system the rest of the
    # projection lives in; square keeps native because it operates in
    # blend coords directly (calibration view).  After scaling, the
    # bake driver tiles `ceil(chord_length / atom_y_extent)` atoms
    # along each `StraightPath` so the rail stays continuous when one
    # atom is shorter than the chord.
    atom_scale: Optional[float]
    # Atlas column count for the output stitch.
    atlas_cols: int


HEX_PROJECTION = Projection(
    name="hex",
    entries=HEX_ENTRIES,
    edge_midpoint=hex_edge_midpoint,
    edge_unit_dir=hex_edge_unit_dir,
    clip_planes=hex_clip_planes,
    for_edges_paths=hex_for_edges_paths,
    ortho_scale=2.0 * HEX_TILE_RADIUS,
    camera_location=(0.0, -10.0, 0.5),
    camera_rotation_euler=(math.radians(90.0), 0.0, 0.0),
    sun_rotation_euler=(math.radians(30.0), 0.0, 0.0),
    extrinsic=hex_proj_shear(),
    atom_scale=INTRA_TILE_PER_BLEND_UNIT,
    atlas_cols=8,
)


# Square projection mirrors the upstream `SQUARE_VIEWPOINT['S']`
# camera pose verbatim (vehicles-alignment, the only alignment
# modelled today — see CLAUDE.md → "Alignment mode is asset-class-
# dependent").  Calibration unverified: a different alignment mode
# would shift the rail's position inside the rendered tile.
SQUARE_PROJECTION = Projection(
    name="square",
    entries=SQUARE_ENTRIES,
    edge_midpoint=square_edge_midpoint,
    edge_unit_dir=square_edge_unit_dir,
    clip_planes=square_clip_planes,
    for_edges_paths=square_for_edges_paths,
    ortho_scale=UPSTREAM_ORTHO_SCALE,
    camera_location=(6.6, -7.9, 11.6),
    camera_rotation_euler=(math.radians(60.0), 0.0, math.radians(45.0)),
    sun_rotation_euler=(math.radians(90.0), 0.0, math.radians(90.0)),
    extrinsic=None,
    atom_scale=None,  # native blend coords; see SQUARE_PROJECTION docstring
    atlas_cols=4,
)


PROJECTIONS: dict[str, Projection] = {
    "hex": HEX_PROJECTION,
    "square": SQUARE_PROJECTION,
}
