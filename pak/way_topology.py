"""Hex way path geometry: where the rail/road/tram goes on each tile.

Per ribi (the set of edges a way connects to), this module emits the
list of `StraightPath` segments that cover the tile — a stub for a
single edge, a chord or V-bend for two edges, a junction (pairwise
chords + V-bends) for three or more.  Pure geometry; the asset's
visual cross-section (ballast, sleepers, paint markings) lives in
the bake driver (`pak/bake_way.py`), which transforms an upstream
blend's mesh atom along each `StraightPath`.

All topology resolves to straight chord pieces — 60° bends are
two-leg V-bends, not arcs, so the bake driver never needs to handle
a curved primitive.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from .way import (
    HEX_CORNERS, HEX_EDGES,
    edge_midpoint, edge_unit_dir, shared_corner,
)


@dataclass
class StraightPath:
    """One straight chord between two points, with cap directions at
    each end.

    `cap_a` / `cap_b` are the unit vectors along which the slab end
    boundaries lie.  The cap line — not the cap direction — is what
    matters: the slab boundary at s=0 runs along `cap_a` through
    `start`, the boundary at s=1 runs along `cap_b` through `end`.
    Interpolating cap offsets (not directions) linearly along s yields
    a straight slab edge for any perpendicular distance, and avoids
    the 1/(cap · perp) singularity V-bend legs would otherwise hit
    when the interpolated direction lands parallel to the chord.

    `skip_cap_a` / `skip_cap_b` flag chord ends meeting another chord
    on the same plane with opposing normals — V-bend apex caps — so
    the bake driver can suppress one of each coplanar pair to avoid
    z-fighting.
    """
    start: tuple[float, float]
    end: tuple[float, float]
    cap_a: tuple[float, float]
    cap_b: tuple[float, float]
    skip_cap_a: bool = False
    skip_cap_b: bool = False


# ---- Path builders --------------------------------------------------------
# Each returns a list of paths the bake driver places the asset's mesh
# atom along.

def between_edges_paths(edge_a: str, edge_b: str) -> list[StraightPath]:
    """Through-tile straight between two edge midpoints, ends mitred
    along the local edge directions.  For opposite edges the chord is
    perpendicular to both and the result is axis-aligned; for non-
    opposite pairs the ends become parallelogram cuts so adjacent
    tiles' ways meet flush at the shared edge midpoint."""
    return [StraightPath(
        start=edge_midpoint(edge_a), end=edge_midpoint(edge_b),
        cap_a=edge_unit_dir(edge_a), cap_b=edge_unit_dir(edge_b))]


def bend_curve_paths(edge_a: str, edge_b: str) -> list[StraightPath]:
    """V-bend between two 60°-apart hex edges sharing one corner.
    The apex sits on the radial through the shared corner at half
    the hex radius — i.e. at `corner / 2` — and the apex miter cap
    is the unit vector toward the corner (which is the bisector of
    the two edge directions there, since the corner is equidistant
    from both edges by hex symmetry).  Each leg is therefore a
    piece of an off-axis through-tile chord: leg A from M_a to the
    apex, parallel to edge_b; leg B from the apex to M_b, parallel
    to edge_a.  Apex caps are suppressed (they're internal and
    would z-fight against each other)."""
    corner = shared_corner(edge_a, edge_b)
    cx, cy = HEX_CORNERS[corner]                       # unit vector
    apex = (cx / 2.0, cy / 2.0)
    apex_cap = (cx, cy)
    return [
        StraightPath(start=edge_midpoint(edge_a), end=apex,
                     cap_a=edge_unit_dir(edge_a), cap_b=apex_cap,
                     skip_cap_b=True),
        StraightPath(start=apex, end=edge_midpoint(edge_b),
                     cap_a=apex_cap, cap_b=edge_unit_dir(edge_b),
                     skip_cap_a=True),
    ]


def curve_paths(edge_a: str, edge_b: str):
    """Two-edge connection: 60°-apart pairs (sharing a corner) →
    V-bend (two off-axis chord pieces); 120° / 180° pairs → mitred
    through-tile chord."""
    if set(HEX_EDGES[edge_a]) & set(HEX_EDGES[edge_b]):
        return bend_curve_paths(edge_a, edge_b)
    return between_edges_paths(edge_a, edge_b)


# Fraction of the centre-to-edge-midpoint distance the stub body
# covers, measured from the edge midpoint inward.  Stubs visibly
# "end on the tile" rather than running flush to the centre — used
# both for flat-ground single-ribi cells and for half-slope stubs
# on ramp tiles.  0.5 = stub covers the outer half of the radial.
STUB_LENGTH_FRACTION = 0.5


def stub_paths(edge: str) -> list[StraightPath]:
    """Short chord from the edge midpoint inward toward the tile centre.
    Length is `STUB_LENGTH_FRACTION` of the centre-to-edge-midpoint
    radial — the stub stops well short of the centre so a single-
    ribi cell visibly terminates inside the tile rather than running
    to its centre.  Edge end mitred along the local edge direction;
    inner end gets a perpendicular cut."""
    end = edge_midpoint(edge)
    n = math.hypot(end[0], end[1])
    cap_centre = (-end[1] / n, end[0] / n)
    start = (end[0] * (1.0 - STUB_LENGTH_FRACTION),
             end[1] * (1.0 - STUB_LENGTH_FRACTION))
    return [StraightPath(start=start, end=end,
                         cap_a=cap_centre, cap_b=edge_unit_dir(edge))]


def junction_paths(edges):
    """N≥3 way junction as the union of all `C(N,2)` pairwise edge
    connections, each routed via `curve_paths` — so 60°-apart pairs
    become V-bends and 120° / 180° pairs become mitred through-tile
    chords.  An asymmetric 3-way like {N, NE, S} reads as one
    straight (N↔S) plus one V-bend (N↔NE) plus one 120° chord
    (NE↔S), instead of three stubs meeting at the centre.
    Through-routes therefore continue as real chords across the
    junction tile."""
    return [path
            for i, a in enumerate(edges)
            for b in edges[i + 1:]
            for path in curve_paths(a, b)]


def for_edges_paths(edges):
    """Dispatch on edge count: 1 → stub, 2 → curve, 3+ → junction.
    The asset's `render_hex_cell(edges)` reduces to building a Model
    and calling `cs.paint(model, for_edges_paths(edges))`."""
    if len(edges) == 1:
        return stub_paths(edges[0])
    if len(edges) == 2:
        return curve_paths(edges[0], edges[1])
    return junction_paths(edges)


# Slope variants (axis-aligned ramps, half-stubs) reduce to a flat-tile
# path + a chord-aligned linear z-tilt.  The bake driver derives them
# from `between_edges_paths` / `stub_paths` + `HEX_OPPOSITE_EDGE` plus
# `pak.hex_synth.engine_z_per_step(steps)` for the total chord rise —
# kept out of this module so it stays painter-agnostic.


# ---- Composition helpers --------------------------------------------------
# The bake driver clones the upstream blend's straight atom (authored
# along +Y, centred at origin, length = through-tile chord) once per
# `StraightPath`, transforms the clone onto the chord, then bisects
# the clone against the cap planes to trim the ends.  Pure math here;
# the actual mesh ops live in `pak/bake_way.py` (Blender-only).


def path_chord_length(path: "StraightPath") -> float:
    """Euclidean length of the chord from `start` to `end`."""
    dx = path.end[0] - path.start[0]
    dy = path.end[1] - path.start[1]
    return math.hypot(dx, dy)


def path_chord_angle(path: "StraightPath") -> float:
    """Z-rotation `θ` such that `R_z(θ) @ (0, 1, 0)` lands along the
    chord direction `(end - start) / |end - start|`.  The atom is
    authored along +Y so this is exactly the angle the bake driver
    rotates each clone by before translating to the chord midpoint."""
    dx = path.end[0] - path.start[0]
    dy = path.end[1] - path.start[1]
    return math.atan2(-dx, dy)


def path_chord_midpoint(path: "StraightPath") -> tuple[float, float]:
    return ((path.start[0] + path.end[0]) / 2.0,
            (path.start[1] + path.end[1]) / 2.0)


def path_chord_unit(path: "StraightPath") -> tuple[float, float]:
    """Unit vector along the chord from `start` to `end`."""
    dx = path.end[0] - path.start[0]
    dy = path.end[1] - path.start[1]
    n = math.hypot(dx, dy)
    return (dx / n, dy / n)


def atom_offsets_along_path(chord_length: float, atom_step: float
                            ) -> list[float]:
    """Return offset-along-chord values for each atom in a multi-atom
    tiling of `chord_length` by atoms of Y-extent `atom_step`.

    Atoms are centred on the chord midpoint (offset 0) and tile end-to-
    end at step `atom_step` so consecutive atoms' near ends meet — when
    the blend's sleepers are spaced symmetrically inside `atom_step`,
    tiling preserves the cadence without gaps or overlaps.  The outer
    atoms overrun the chord ends; `pak/bake_way.py`'s cap-plane bisect
    trims them.  Always returns at least one offset (= 0.0), so a stub
    shorter than one atom still emits a single clone the cap bisect
    can crop.

    >>> atom_offsets_along_path(chord_length=1.7, atom_step=0.7)
    [-0.7, 0.0, 0.7]
    >>> atom_offsets_along_path(chord_length=0.4, atom_step=0.7)
    [0.0]
    """
    n = max(1, math.ceil(chord_length / atom_step))
    half_span = (n - 1) / 2 * atom_step
    return [-half_span + k * atom_step for k in range(n)]


def cap_plane(path: "StraightPath", end: str
              ) -> tuple[tuple[float, float], tuple[float, float]] | None:
    """`(plane_co, plane_no)` in world XY for the bisect plane at one
    chord end, or `None` if the cap is suppressed (V-bend apex pair).
    `end` is `'a'` (the `start` cap) or `'b'` (the `end` cap).
    `plane_no` points **inward** — toward the chord midpoint — so a
    bisect that clears the half-space opposite the normal removes the
    overrun beyond the cap line and keeps the chord interior."""
    if end == "a":
        if path.skip_cap_a:
            return None
        cap = path.cap_a
        co = path.start
        toward = (path.end[0] - path.start[0], path.end[1] - path.start[1])
    elif end == "b":
        if path.skip_cap_b:
            return None
        cap = path.cap_b
        co = path.end
        toward = (path.start[0] - path.end[0], path.start[1] - path.end[1])
    else:
        raise ValueError(f"cap_plane: end={end!r} (expected 'a' or 'b')")
    # Perpendicular to the cap direction in XY.  The cap LINE runs
    # along `cap` through `co`; the bisect plane contains that line and
    # the world Z axis, so its normal is one of the two perpendiculars
    # to `cap` in XY.  Pick the one with positive dot toward the chord
    # midpoint (the half-space we keep).
    n1 = (-cap[1], cap[0])
    n2 = ( cap[1], -cap[0])
    if n1[0] * toward[0] + n1[1] * toward[1] >= 0.0:
        normal = n1
    else:
        normal = n2
    return (co, normal)
