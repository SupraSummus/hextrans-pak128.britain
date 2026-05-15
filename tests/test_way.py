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

from pak.way import (
    HEX_ENTRIES,
    HEX_TILE_RADIUS,
    SLOPE_HEX_DOUBLE_ENTRIES,
    SLOPE_HEX_ENTRIES,
    SLOPE_HEX_HALF_DOUBLE_ENTRIES,
    SLOPE_HEX_HALF_ENTRIES,
    ribi_edges,
    ribi_label,
)
from pak.way import edge_midpoint
from pak.way_topology import for_edges_paths, stub_paths


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


class WorldScale(unittest.TestCase):
    """The hex world unit is the tile entry-edge length, equal to one
    square pak tile side — `pak/bake_way.py` scales the blend mesh
    against this constant so the per-tile geometry stays consistent
    across way ports."""

    def test_world_radius_is_one(self):
        self.assertEqual(HEX_TILE_RADIUS, 1.0)


if __name__ == "__main__":
    unittest.main()
