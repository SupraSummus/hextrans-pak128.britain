"""Tests for the way ribi / slope vocabulary and topology dispatch.

The vocabulary side (`pak.way`) is the engine contract — every label
here has to round-trip through `way_image_keys.cc::ribi_key` and
`slope_slot_keys`.  The topology side (`pak.way_topology.for_edges_paths`)
is the per-ribi composition shape `pak/bake_way.py` walks when it
composes the upstream blend's straight atom into V-bends / junctions /
stubs across the 63 hex ribi cells.

Pure-data tests; the Cycles render path lives in `pak/bake_way.py`
and runs only inside Blender, so it isn't covered here.  See CLAUDE.md
→ "Way-bake architecture".

Run from the repo root:

    python3 -m pytest tests/

or, without pytest installed:

    python3 -m unittest tests.test_way
"""

from __future__ import annotations

import unittest

import math

from pak.way import (
    HEX_ENTRIES,
    HEX_TILE_RADIUS,
    SLOPE_HEX_DOUBLE_ENTRIES,
    SLOPE_HEX_ENTRIES,
    SLOPE_HEX_HALF_DOUBLE_ENTRIES,
    SLOPE_HEX_HALF_ENTRIES,
    hex_clip_planes,
    ribi_edges,
    ribi_label,
)
from pak.way import edge_midpoint
from pak.way_topology import (
    atom_offsets_along_path,
    cap_plane,
    for_edges_paths,
    path_chord_angle,
    path_chord_length,
    path_chord_midpoint,
    stub_paths,
)


class RibiVocabulary(unittest.TestCase):
    """`way_image_keys.cc::ribi_key` contract: 63 non-zero ribis, bit
    names lower-case, joined low-bit-first by `_`.  Order in
    `HEX_ENTRIES` is popcount-then-ribi (matches the engine writer's
    iteration order and the .dat key order in the worked example
    `rail_060_tracks.dat`)."""

    def test_count(self):
        self.assertEqual(len(HEX_ENTRIES), 63)

    def test_zero_is_dash(self):
        self.assertEqual(ribi_label(0), "-")
        self.assertEqual(ribi_edges(0), ())

    def test_first_six_are_singletons_clockwise_from_se(self):
        # ribi bits: SE=0, S=1, SW=2, NW=3, N=4, NE=5
        first = [label for label, _ in HEX_ENTRIES[:6]]
        self.assertEqual(first, ["se", "s", "sw", "nw", "n", "ne"])

    def test_popcount_order(self):
        # Entries are sorted by (popcount, ribi) — same order the engine
        # writer keys against, so atlas cell index `i` lands at row
        # `i // 8`, col `i % 8` in a standard 8-wide atlas.
        popcounts = [len(edges) for _, edges in HEX_ENTRIES]
        self.assertEqual(popcounts, sorted(popcounts))

    def test_se_s_label(self):
        # 0b011 = SE | S
        self.assertEqual(ribi_label(0b011), "se_s")
        self.assertEqual(ribi_edges(0b011), ("SE", "S"))

    def test_full_six_way_label(self):
        # 0b111111 = all edges
        self.assertEqual(ribi_label(0b111111), "se_s_sw_nw_n_ne")


class SlopeVocabulary(unittest.TestCase):
    """Slope slot keys mirror `way_image_keys.cc::slope_slot_keys`."""

    def test_full_set_sizes(self):
        self.assertEqual(len(SLOPE_HEX_ENTRIES), 6)
        self.assertEqual(len(SLOPE_HEX_DOUBLE_ENTRIES), 6)
        self.assertEqual(len(SLOPE_HEX_HALF_ENTRIES), 12)
        self.assertEqual(len(SLOPE_HEX_HALF_DOUBLE_ENTRIES), 12)

    def test_full_axis_order_clockwise_from_north(self):
        labels = [label for label, _ in SLOPE_HEX_ENTRIES]
        self.assertEqual(labels, ["n", "ne", "se", "s", "sw", "nw"])

    def test_double_labels_have_suffix(self):
        for (single, edge_a), (double, edge_b) in zip(
                SLOPE_HEX_ENTRIES, SLOPE_HEX_DOUBLE_ENTRIES):
            self.assertEqual(edge_a, edge_b)
            self.assertEqual(double, f"{single}_double")

    def test_half_label_shape(self):
        # First 6 are low halves, next 6 are high halves.
        self.assertTrue(SLOPE_HEX_HALF_ENTRIES[0][0].endswith("_low_half"))
        self.assertFalse(SLOPE_HEX_HALF_ENTRIES[0][2])
        self.assertTrue(SLOPE_HEX_HALF_ENTRIES[6][0].endswith("_high_half"))
        self.assertTrue(SLOPE_HEX_HALF_ENTRIES[6][2])


class TopologyDispatch(unittest.TestCase):
    """`for_edges_paths` returns 1 stub for single-edge, 1 or 2 chords
    for two-edge (60° → V-bend = 2 legs, 120°/180° → 1 chord), and one
    chord per pair for 3+-edge junctions."""

    def test_stub_returns_one_path(self):
        self.assertEqual(len(for_edges_paths(("N",))), 1)

    def test_opposite_pair_one_chord(self):
        self.assertEqual(len(for_edges_paths(("N", "S"))), 1)

    def test_adjacent_pair_v_bend(self):
        # N and NE share corner; V-bend gives 2 legs.
        self.assertEqual(len(for_edges_paths(("N", "NE"))), 2)

    def test_three_way_junction_path_count(self):
        # C(3, 2) = 3 pairs.  N↔S is opposite → 1 chord.  N↔NE shares
        # corner NE → 2-leg V-bend.  S↔NE shares no corner (S touches
        # SW/SE, NE touches E/NE) → 120°-apart, 1 chord.  Total = 4.
        paths = for_edges_paths(("N", "S", "NE"))
        self.assertEqual(len(paths), 4)

    def test_six_way_junction_path_count(self):
        # C(6, 2) = 15 pairs.  3 are opposite (single chord each = 3);
        # 6 are 60°-adjacent (V-bend = 2 legs each = 12); 6 are
        # 120°-apart (single chord each = 6).  Total = 3 + 12 + 6 = 21.
        paths = for_edges_paths(("SE", "S", "SW", "NW", "N", "NE"))
        self.assertEqual(len(paths), 21)


class PathCoordinates(unittest.TestCase):
    """Topology builders place chord endpoints at the right tile
    landmarks — edge midpoints for chords, partway-along the radial
    for stubs."""

    def test_stub_ends_at_edge_midpoint(self):
        path = stub_paths("N")[0]
        self.assertEqual(path.end, edge_midpoint("N"))

    def test_stub_start_is_on_radial(self):
        # `stub_paths` lays a chord from STUB_LENGTH_FRACTION-of-way-in
        # toward the edge midpoint; start should be the midpoint scaled
        # by (1 - STUB_LENGTH_FRACTION).
        from pak.way_topology import STUB_LENGTH_FRACTION
        mx, my = edge_midpoint("N")
        sx, sy = stub_paths("N")[0].start
        scale = 1.0 - STUB_LENGTH_FRACTION
        self.assertAlmostEqual(sx, mx * scale)
        self.assertAlmostEqual(sy, my * scale)


class ChordTransform(unittest.TestCase):
    """`path_chord_angle` is the Z rotation such that the atom's +Y axis
    lines up with the chord direction; `path_chord_midpoint` and
    `path_chord_length` are the chord's centre + Euclidean span."""

    def test_north_south_chord(self):
        # N edge midpoint to S edge midpoint — atom should rotate 180°
        # (atom +Y points south after rotation), centre at origin,
        # length = R*sqrt(3).
        path = for_edges_paths(("N", "S"))[0]
        self.assertAlmostEqual(path_chord_length(path), math.sqrt(3.0))
        self.assertAlmostEqual(path_chord_midpoint(path)[0], 0.0)
        self.assertAlmostEqual(path_chord_midpoint(path)[1], 0.0)
        angle = path_chord_angle(path)
        # R_z(angle) @ (0, 1, 0) should be (0, -1, 0).
        self.assertAlmostEqual(-math.sin(angle), 0.0)
        self.assertAlmostEqual(math.cos(angle), -1.0)

    def test_stub_chord_direction(self):
        # Stub from inside the tile out to the N edge — atom +Y rotates
        # to point north (toward +Y), so angle ≈ 0.
        path = stub_paths("N")[0]
        angle = path_chord_angle(path)
        self.assertAlmostEqual(-math.sin(angle), 0.0, places=6)
        self.assertAlmostEqual(math.cos(angle), 1.0, places=6)

    # `chord_length_matches_endpoints` lives on the projection-
    # agnostic mixin (`HexInvariants`, `SquareInvariants`).


class AtomTiling(unittest.TestCase):
    """`atom_offsets_along_path` returns chord-offset slots for each
    atom in a multi-atom tiling.  `pak/bake_way.py` consumes this when
    one atom is shorter than the chord and the rail needs to stay
    continuous along the path."""

    def test_short_chord_emits_one_centred_atom(self):
        # Chord much shorter than atom step → single atom at the
        # midpoint; the cap bisect handles the overrun.
        self.assertEqual(atom_offsets_along_path(0.4, 0.7), [0.0])

    def test_atoms_centred_on_chord_midpoint(self):
        # Symmetric around 0: a 3-atom run at step 0.7 sits at
        # {-0.7, 0.0, +0.7}.
        offsets = atom_offsets_along_path(1.7, 0.7)
        self.assertEqual(len(offsets), 3)
        self.assertEqual(sum(offsets), 0.0)
        for k in range(len(offsets) - 1):
            self.assertAlmostEqual(offsets[k + 1] - offsets[k], 0.7)

    def test_count_covers_chord(self):
        # n = ceil(chord / step); n atoms span n*step ≥ chord.
        for chord, step in [(0.5, 0.7), (1.0, 0.7), (1.7, 0.7),
                            (2.0, 0.7), (2.1, 0.7), (3.5, 0.7)]:
            offsets = atom_offsets_along_path(chord, step)
            self.assertGreaterEqual(len(offsets) * step, chord)
            # n-1 step span ≤ chord (one fewer wouldn't cover).
            self.assertLess((len(offsets) - 1) * step, chord + 1e-9)

    def test_zero_length_chord_emits_one_atom(self):
        # Edge case the topology layer doesn't actually produce, but
        # the helper must not divide-by-zero on it.
        self.assertEqual(atom_offsets_along_path(0.0, 0.7), [0.0])


class CapPlanes(unittest.TestCase):
    """`cap_plane(path, end)` returns `(plane_co, plane_no)` in world XY
    with `plane_no` pointing inward (toward the chord midpoint), so a
    bisect that clears the half-space opposite the normal removes
    overrun beyond the cap and keeps the path interior."""

    def test_skip_returns_none(self):
        # 60°-adjacent V-bend → apex caps suppressed.
        paths = for_edges_paths(("N", "NE"))
        self.assertEqual(len(paths), 2)
        self.assertIsNone(cap_plane(paths[0], "b"))  # leg A's apex cap
        self.assertIsNone(cap_plane(paths[1], "a"))  # leg B's apex cap


# ---- Projection-parametric invariants --------------------------------------
# The cap-plane / clip-plane / chord-length contracts are projection-
# agnostic — the bake driver's bisect calls (`pak/bake_way.py::_bisect_mesh`
# with `clear_inner=True`) depend on every plane normal pointing inward,
# regardless of whether the tile is hex or square.  Express the contract
# once as a mixin, instantiate twice.

class _ProjectionInvariants:
    """Mixin asserting `pak/bake_way.py`'s composition contracts hold
    across the full ribi list.  Subclasses set `entries` (popcount-then-
    ribi list of `(label, edges)`), `for_edges_paths` (path dispatch
    callable), and `clip_planes` (tile-outline plane builder)."""

    entries: list
    for_edges_paths: staticmethod
    clip_planes: staticmethod

    def _paths(self):
        for _, edges in self.entries:
            for path in self.for_edges_paths(edges):
                yield path

    def test_chord_length_matches_endpoints(self):
        for path in self._paths():
            dx = path.end[0] - path.start[0]
            dy = path.end[1] - path.start[1]
            self.assertAlmostEqual(path_chord_length(path),
                                   math.hypot(dx, dy))

    def test_cap_normal_points_inward(self):
        for path in self._paths():
            for end in ("a", "b"):
                cp = cap_plane(path, end)
                if cp is None:
                    continue
                _, (nx, ny) = cp
                if end == "a":
                    toward = (path.end[0] - path.start[0],
                              path.end[1] - path.start[1])
                else:
                    toward = (path.start[0] - path.end[0],
                              path.start[1] - path.end[1])
                self.assertGreater(nx * toward[0] + ny * toward[1], 0.0)

    def test_cap_normal_perpendicular_to_cap_dir(self):
        for path in self._paths():
            for end, cap in (("a", path.cap_a), ("b", path.cap_b)):
                cp = cap_plane(path, end)
                if cp is None:
                    continue
                _, (nx, ny) = cp
                self.assertAlmostEqual(nx * cap[0] + ny * cap[1], 0.0)
                self.assertAlmostEqual(math.hypot(nx, ny), 1.0)

    def test_clip_plane_normals_point_inward(self):
        for (cx, cy), (nx, ny) in self.clip_planes():
            # Origin sits on the +normal side, the side bisect keeps.
            self.assertGreater((0.0 - cx) * nx + (0.0 - cy) * ny, 0.0)
            self.assertAlmostEqual(math.hypot(nx, ny), 1.0)


class HexInvariants(_ProjectionInvariants, unittest.TestCase):
    entries = HEX_ENTRIES
    for_edges_paths = staticmethod(for_edges_paths)
    clip_planes = staticmethod(hex_clip_planes)


class SquareInvariants(_ProjectionInvariants, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Late-bind so importing this test module doesn't pull
        # `way_proj` (which transitively pulls numpy via `hex_synth`)
        # at collection time on pure-stdlib runs.
        from pak.way_proj import SQUARE_PROJECTION
        cls.entries = SQUARE_PROJECTION.entries
        cls.for_edges_paths = staticmethod(SQUARE_PROJECTION.for_edges_paths)
        cls.clip_planes = staticmethod(SQUARE_PROJECTION.clip_planes)


class HexClipPlanesGeometry(unittest.TestCase):
    """Hex-specific clip-plane facts: count + apothem distance.  The
    inward-normal invariant is covered by `HexInvariants`."""

    def test_six_planes(self):
        self.assertEqual(len(hex_clip_planes()), 6)

    def test_planes_pass_through_edge_midpoints(self):
        # Each plane_co at the apothem = sqrt(3)/2 from origin.
        for (cx, cy), _ in hex_clip_planes():
            self.assertAlmostEqual(math.hypot(cx, cy), math.sqrt(3.0) / 2.0)


class SquareProjection(unittest.TestCase):
    """Square-specific facts: ribi enumeration + canonical labels +
    bend topology.  The projection-agnostic invariants are covered by
    `SquareInvariants`."""

    @classmethod
    def setUpClass(cls):
        from pak.way_proj import SQUARE_PROJECTION
        cls.proj = SQUARE_PROJECTION

    def test_fifteen_entries(self):
        # 2^4 - 1 = 15 non-empty edge subsets.
        self.assertEqual(len(self.proj.entries), 15)

    def test_singletons_first(self):
        first = {label for label, _ in self.proj.entries[:4]}
        self.assertEqual(first, {"N", "S", "E", "W"})

    def test_canonical_labels(self):
        labels = {label for label, _ in self.proj.entries}
        for key in ("NS", "EW", "NE", "NW", "SE", "SW",
                    "NSE", "NSW", "NEW", "SEW", "NSEW"):
            self.assertIn(key, labels)

    def test_ns_chord_through_origin(self):
        paths = self.proj.for_edges_paths(("N", "S"))
        self.assertEqual(len(paths), 1)
        mx, my = path_chord_midpoint(paths[0])
        self.assertAlmostEqual(mx, 0.0)
        self.assertAlmostEqual(my, 0.0)

    def test_ne_bend_two_legs(self):
        # 90°-adjacent edges share a corner → V-bend approximation.
        self.assertEqual(len(self.proj.for_edges_paths(("N", "E"))), 2)

    def test_four_way_junction_path_count(self):
        # C(4, 2) = 6 pairs: 2 opposite (1 chord each) + 4 adjacent
        # (V-bend = 2 legs each) = 2 + 8 = 10 paths.
        self.assertEqual(len(self.proj.for_edges_paths(("N", "E", "S", "W"))), 10)


class WorldScale(unittest.TestCase):
    """The hex world unit is the tile entry-edge length, equal to one
    square pak tile side — `pak/bake_way.py` scales the blend mesh
    against this constant so the per-tile geometry stays consistent
    across way ports."""

    def test_world_radius_is_one(self):
        self.assertEqual(HEX_TILE_RADIUS, 1.0)


if __name__ == "__main__":
    unittest.main()
