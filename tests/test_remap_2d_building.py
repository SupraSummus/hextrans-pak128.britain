"""Pin the 4-hex rhombus geometry that `remap_2d_building` ships.

Earlier in the design we shipped two "different" orientations whose
axial cells reduced to the same edge direction (the (1,-1) family);
the visual diff caught it but a deterministic shape check is cheaper.
"""

from __future__ import annotations

import math
import unittest

import numpy as np

from pak.hex_split import hex_tile_screen_offset, stitch as hex_stitch
from pak.remap_2d_building import MAGIC_PINK, RHOMBUS_ORIENTATIONS, _split_hex

R = 1.0
SQRT3 = math.sqrt(3.0)


def _axial_to_world(q: int, r: int) -> tuple[float, float]:
    return (1.5 * R * q, 0.5 * SQRT3 * R * q + SQRT3 * R * r)


def _hex_contains(qr: tuple[int, int], pt: tuple[float, float]) -> bool:
    cx, cy = _axial_to_world(*qr)
    dx, dy = pt[0] - cx, pt[1] - cy
    # Flat-top hex: |y| ≤ √3/2 R AND |x| + |y|/√3 ≤ R.
    return (abs(dy) <= (SQRT3 / 2) * R + 1e-9
            and abs(dx) + abs(dy) / SQRT3 <= R + 1e-9)


def _centroid(cells: list[tuple[int, int]]) -> tuple[float, float]:
    xs, ys = zip(*(_axial_to_world(q, r) for q, r in cells), strict=True)
    return sum(xs) / len(xs), sum(ys) / len(ys)


class TestRhombusOrientations(unittest.TestCase):
    def test_three_distinct_orientations(self):
        # Each orientation defines a different shared interior edge,
        # so the set of (sorted) axial cells must differ across all three.
        keys = [tuple(sorted(c)) for c in RHOMBUS_ORIENTATIONS.values()]
        self.assertEqual(len(set(keys)), 3)

    def test_c2_symmetric_about_centroid(self):
        # 180° rotation about the centroid must map each cell to another
        # cell in the same cluster.
        for name, cells in RHOMBUS_ORIENTATIONS.items():
            cx, cy = _centroid(cells)
            world = {_axial_to_world(q, r) for q, r in cells}
            for wx, wy in list(world):
                mirror = (2 * cx - wx, 2 * cy - wy)
                self.assertTrue(
                    any(math.hypot(mx - mirror[0], my - mirror[1]) < 1e-6
                        for mx, my in world),
                    f"{name}: ({wx},{wy}) has no C2 partner",
                )

    def test_diamond_corners_contained(self):
        # 2x2 square rotated 45° → diamond with corners √2·R from centroid
        # on the cardinal axes.  Each corner must land inside one of the
        # cluster's hexes.
        for name, cells in RHOMBUS_ORIENTATIONS.items():
            cx, cy = _centroid(cells)
            d = math.sqrt(2.0) * R
            corners = [(cx + d, cy), (cx - d, cy),
                       (cx, cy + d), (cx, cy - d)]
            for pt in corners:
                self.assertTrue(
                    any(_hex_contains(qr, pt) for qr in cells),
                    f"{name}: corner {pt} not in any cluster cell",
                )


class TestCentroidIsEdgeMidpoint(unittest.TestCase):
    def test_centroid_lies_on_a_shared_edge(self):
        # The cluster centroid must coincide with the midpoint of the
        # shared edge between exactly one pair of cluster cells.  This
        # is what gives the 4-hex rhombus its "centred" property.
        sqrt3R = SQRT3 * R
        for name, cells in RHOMBUS_ORIENTATIONS.items():
            cx, cy = _centroid(cells)
            shared_pairs = []
            for i, a in enumerate(cells):
                for b in cells[i + 1:]:
                    ax_, ay_ = _axial_to_world(*a)
                    bx_, by_ = _axial_to_world(*b)
                    if abs(math.hypot(ax_ - bx_, ay_ - by_) - sqrt3R) < 1e-6:
                        mx, my = (ax_ + bx_) / 2, (ay_ + by_) / 2
                        if math.hypot(mx - cx, my - cy) < 1e-6:
                            shared_pairs.append((a, b))
            self.assertEqual(len(shared_pairs), 1,
                             f"{name}: expected exactly 1 shared edge "
                             f"through centroid, got {len(shared_pairs)}")


class TestScreenOffsetsMatchAxial(unittest.TestCase):
    def test_screen_centroid_under_hex_tile_offset(self):
        # The driver computes the cluster centroid in screen px via
        # hex_tile_screen_offset.  Sanity-check that the centroid in
        # world-axial space and in screen-px space agree on which
        # cluster pair is the central edge.
        for name, cells in RHOMBUS_ORIENTATIONS.items():
            offsets = [hex_tile_screen_offset(q, r) for q, r in cells]
            xs, ys = zip(*offsets, strict=True)
            sx, sy = sum(xs) / 4, sum(ys) / 4
            # Two cluster hexes must lie equidistant from the screen
            # centroid (the shared-edge pair).
            dists = sorted(math.hypot(ox - sx, oy - sy) for ox, oy in offsets)
            self.assertAlmostEqual(dists[0], dists[1], places=6,
                                   msg=f"{name}: nearest pair not equidistant")


class TestSplitRoundtrip(unittest.TestCase):
    """`_split_hex` then `pak.hex_split.stitch` must recover the source
    canvas on every claimed pixel.  Pins the rhombus integration; the
    cutter's own partition invariant is pinned in `test_sq_split`."""

    def _restitch(self, hex_cells, orientation):
        # Inverse of `_split_hex`: same anchors, hand the per-cell sprites
        # to `pak.hex_split.stitch`.  Mirrors the production split path.
        cells_ax = RHOMBUS_ORIENTATIONS[orientation]
        offsets = [hex_tile_screen_offset(q, r) for q, r in cells_ax]
        cent_x = sum(o[0] for o in offsets) / len(offsets)
        cent_y = sum(o[1] for o in offsets) / len(offsets)
        anchors = {(q, r, 0): (int(round(ox - cent_x)) + 256,
                               int(round(oy - cent_y)) + 256)
                   for (q, r), (ox, oy) in zip(cells_ax, offsets, strict=True)}
        cells_dict = {(q, r, 0): cell
                      for (q, r), cell in zip(cells_ax, hex_cells, strict=True)}
        canvas = np.empty((512, 512, 4), dtype=np.uint8)
        canvas[..., :3] = MAGIC_PINK
        canvas[..., 3] = 255
        hex_stitch(cells_dict, anchors, into_canvas=canvas)
        return canvas

    def test_roundtrip_preserves_claimed_pixels(self):
        # Deterministic non-MAGIC_PINK gradient so collisions don't
        # mask roundtrip mismatches.  Cluster centre at (256, 256).
        ys, xs = np.indices((512, 512))
        canvas = np.empty((512, 512, 4), dtype=np.uint8)
        canvas[..., 0] = (xs * 200 // 511).astype(np.uint8)
        canvas[..., 1] = (ys * 200 // 511).astype(np.uint8)
        canvas[..., 2] = ((xs + ys) * 100 // 1022).astype(np.uint8)
        canvas[..., 3] = 255

        for orientation in RHOMBUS_ORIENTATIONS:
            with self.subTest(orientation=orientation):
                hex_cells = _split_hex(canvas, orientation)
                reassembled = self._restitch(hex_cells, orientation)
                covered = (reassembled[..., :3] != np.array(MAGIC_PINK)).any(axis=-1)
                # At least the inner 200x200 patch must be covered --
                # protects against an empty/degenerate partition.
                self.assertGreater(covered.sum(), 200 * 200)
                np.testing.assert_array_equal(
                    reassembled[covered], canvas[covered],
                    err_msg=f"{orientation}: roundtrip lost pixels",
                )

if __name__ == "__main__":
    unittest.main()
