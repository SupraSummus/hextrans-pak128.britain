"""Pin the 4-hex rhombus geometry that `remap_2d_building` ships.

Earlier in the design we shipped two "different" orientations whose
axial cells reduced to the same edge direction (the (1,-1) family);
the visual diff caught it but a deterministic shape check is cheaper.
"""

from __future__ import annotations

import math
import unittest

import numpy as np

from pak.remap_2d_building import (
    _CELL_GROUND_ANCHOR,
    MAGIC_PINK,
    RHOMBUS_ORIENTATIONS,
    W,
    _split_hex,
)
from pak.viewpoints import hex_cell_shape_mask, hex_tile_screen_offset, hex_voronoi_mask

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
    """Split→restitch must preserve every pixel the cluster's Voronoi
    partition claims (not just the within-hex-shape band).  Catches
    regressions that would crop the building's upper part to
    MAGIC_PINK by ANDing in `hex_cell_shape_mask`."""

    def _restitch(self, hex_cells, orientation):
        offsets = [hex_tile_screen_offset(q, r)
                   for q, r in RHOMBUS_ORIENTATIONS[orientation]]
        cent_x = sum(o[0] for o in offsets) / len(offsets)
        cent_y = sum(o[1] for o in offsets) / len(offsets)
        rel = [(int(round(ox - cent_x)), int(round(oy - cent_y)))
               for ox, oy in offsets]
        canvas = np.empty((512, 512, 4), dtype=np.uint8)
        canvas[..., :3] = MAGIC_PINK
        canvas[..., 3] = 255
        ccx, ccy = 256, 256
        ax, ay = _CELL_GROUND_ANCHOR
        for (dx, dy), cell in zip(rel, hex_cells, strict=True):
            y0, x0 = ccy + dy - ay, ccx + dx - ax
            keyed = (cell[..., :3] == np.array(MAGIC_PINK)).all(axis=-1)
            sub = canvas[y0:y0 + W, x0:x0 + W]
            sub[~keyed] = cell[~keyed]
        return canvas

    def test_roundtrip_preserves_voronoi_pixels(self):
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

    def test_voronoi_keeps_more_than_cell_shape(self):
        # `hex_voronoi_mask` keeps the full Voronoi cell; ANDing the
        # cell-shape clip on top can only shrink it -- if it's equal
        # something else broke.
        voronoi = hex_voronoi_mask((0, 0), [(96, 32), (0, 64), (96, 96)],
                                   image_width=W)
        clipped = voronoi * hex_cell_shape_mask(image_width=W)
        self.assertGreater(voronoi.sum(), clipped.sum())


if __name__ == "__main__":
    unittest.main()
