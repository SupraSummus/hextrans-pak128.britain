"""Tests for `pak.square_synth.SquareGeom`.

Pinned against the upstream pak128.Britain `texture-lightmap.png`
cell layout (reverse-engineered in CLAUDE.md / square_synth's
module docstring) so a future refactor of the projection has to
re-justify its geometry against the same authored ground truth
the diff harness compares against at run time.
"""

from __future__ import annotations

import unittest

from pak.hex_synth import find_min_partition
from pak.square_synth import (
    NE, NW, SE, SW,
    SQUARE_SLOPE_COUNT,
    SquareGeom,
    square_decode_corner_heights,
    square_iter_valid_slopes,
    square_slope_is_valid,
)


class TestSlopeEncoding(unittest.TestCase):
    """Slope IDs and base-3 corner weights from upstream `landscape/ground.dat`."""

    def test_slope_count_is_eighty_one(self):
        self.assertEqual(SQUARE_SLOPE_COUNT, 81)

    def test_flat_decodes_to_all_zero(self):
        self.assertEqual(square_decode_corner_heights(0), [0, 0, 0, 0])

    def test_single_corner_weights(self):
        # Image[1]=sw1, Image[3]=se1, Image[9]=ne1, Image[27]=nw1.
        self.assertEqual(square_decode_corner_heights(1)[SW], 1)
        self.assertEqual(square_decode_corner_heights(3)[SE], 1)
        self.assertEqual(square_decode_corner_heights(9)[NE], 1)
        self.assertEqual(square_decode_corner_heights(27)[NW], 1)

    def test_all_corners_at_two_is_slope_eighty(self):
        self.assertEqual(square_decode_corner_heights(80), [2, 2, 2, 2])


class TestSlopeValidity(unittest.TestCase):
    """`square_slope_is_valid` mirrors hex `slope_is_valid` — min(ch)==0 plus
    adjacent-corner-difference ≤ 2."""

    def test_flat_is_valid(self):
        self.assertTrue(square_slope_is_valid(0))

    def test_non_normalised_rejected(self):
        # Image[40] = all corners at 1 = flat elevation duplicate.
        self.assertFalse(square_slope_is_valid(40))
        # Image[80] = all corners at 2 = same.
        self.assertFalse(square_slope_is_valid(80))

    def test_iter_count_matches_diff_harness(self):
        # 65 normalised + adjacency-valid slopes — matches what
        # diff_grounds.py compares against upstream.
        self.assertEqual(sum(1 for _ in square_iter_valid_slopes()), 65)

    def test_double_slope_is_valid(self):
        # ns2 (Image[8] = se2,sw2): both south corners at 2, north at 0.
        # Adjacent diff = 2 (the double-slope cap), still valid.
        self.assertTrue(square_slope_is_valid(8))


class TestScreenLayout(unittest.TestCase):
    """Lozenge corner positions match upstream's `texture-lightmap.png` cells
    at the default `raster_w=128`."""

    def setUp(self):
        self.geom = SquareGeom()

    def test_canvas_is_one_two_eight_square(self):
        self.assertEqual((self.geom.w, self.geom.h), (128, 128))

    def test_step_lift_is_sixteen_px(self):
        self.assertEqual(self.geom.lift, 16)

    def test_flat_corners_match_upstream_lozenge(self):
        # The upstream flat cell (`Image[0][0]=texture-lightmap.0.14`)
        # places lozenge corners at the screen apexes below.
        self.assertEqual(self.geom.vx, [0, 64, 127, 64])
        self.assertEqual(self.geom.vy_base, [96, 127, 96, 64])

    def test_single_corner_lift_subtracts_sixteen_y(self):
        # nw1 lifts the top apex by one step → y goes from 64 to 48.
        self.assertEqual(self.geom.lifted_vy(27)[NW], 48)
        # ne1 lifts the right apex by one step → y goes from 96 to 80.
        self.assertEqual(self.geom.lifted_vy(9)[NE], 80)


class TestPartition(unittest.TestCase):
    """Generic `find_min_partition` against the square geom — exercises the
    shared partition algorithm from the Geom-agnostic refactor."""

    def setUp(self):
        self.geom = SquareGeom()

    def test_flat_is_single_region(self):
        regions = find_min_partition(0, self.geom)
        self.assertEqual(regions, [[SW, SE, NE, NW]])

    def test_north_south_ramp_stays_single_region(self):
        # ns2 (slope 8) — south edge at z=2, north edge at z=0; all four
        # corners coplanar so no diagonal split needed.
        regions = find_min_partition(8, self.geom)
        self.assertEqual(len(regions), 1)

    def test_single_corner_lift_splits_into_two_triangles(self):
        # sw1 (slope 1) — single corner raised, must split along one
        # diagonal into the flat triangle vs the slanted one.
        regions = find_min_partition(1, self.geom)
        self.assertEqual(len(regions), 2)
        for r in regions:
            self.assertEqual(len(r), 3)


class TestGeomInterface(unittest.TestCase):
    """SquareGeom and HexGeom expose the same Geom interface attrs, so the
    generic helpers can read them by attribute without isinstance branching."""

    def test_required_class_attrs(self):
        for attr in ("corner_count", "corner_labels", "corner_world_xy",
                     "corner_projected_xy", "all_chords", "full_path"):
            self.assertTrue(hasattr(SquareGeom, attr), f"missing {attr}")

    def test_required_instance_attrs(self):
        g = SquareGeom()
        for attr in ("w", "h", "lift", "vx", "vy_base"):
            self.assertTrue(hasattr(g, attr), f"missing {attr}")

    def test_required_methods(self):
        g = SquareGeom()
        # Bound to the instance (lifted_vy reads vy_base/lift) plus the
        # static slope helpers.
        g.lifted_vy(0)
        SquareGeom.decode_corner_heights(0)
        list(SquareGeom.iter_valid_slopes())
        SquareGeom.slope_is_valid(0)


if __name__ == "__main__":
    unittest.main()
