"""Structural pins for `pak.sq_to_hex`.

The algorithm enumerates seven anchor placements and the cell-count
property of the surviving footprints is sensitive to changes in either
the anchor table or the hex-cell rasteriser; these tests catch obvious
regressions in either.
"""

from __future__ import annotations

import unittest

from pak.sq_to_hex import sq_to_hex_all_minimal, sq_to_hex_footprint


class TestSqToHex(unittest.TestCase):
    def test_1x1_single_cell_at_tile_center(self):
        fp = sq_to_hex_footprint(1, 1)
        self.assertEqual(fp.cells, ((0, 0),))
        self.assertEqual(fp.anchor_kind, "tile_center")

    def test_2x2_is_four_cell_rhombus(self):
        fp = sq_to_hex_footprint(2, 2)
        self.assertEqual(set(fp.cells), {(0, 0), (0, 1), (1, 0), (1, 1)})

    def test_2x2_has_three_minimal_orientations(self):
        # Sq's 45° D2 symmetry pins exactly 3 edge-midpoint placements
        # tied for 4-cell footprint -- one per edge orbit
        # (horizontal / slash / backslash).
        opts = sq_to_hex_all_minimal(2, 2)
        self.assertEqual(len(opts), 3)
        self.assertTrue(all(fp.n_cells == 4 for fp in opts))
        self.assertEqual(
            {fp.anchor_kind for fp in opts},
            {"edge_horizontal", "edge_slash", "edge_backslash"},
        )


if __name__ == "__main__":
    unittest.main()
