"""Tests for `pak.diff` -- the shared numerical/image primitives used
by every per-asset-class diff harness (diff_upstream, diff_buildings,
diff_trees, diff_grounds, diff_fence).

The Blender-driven render half is exercised end-to-end via
`python3 -m pak.check <bake_script>`; these tests cover the small
mask/IoU/dRGB/XOR utilities that every harness composes over.

Run from the repo root:

    python3 -m unittest tests.test_diff
"""

from __future__ import annotations

import math
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from pak.diff import (
    MAGIC_PINK,
    GridCell,
    cell_metric,
    compose_grid,
    drgb_intersection,
    iou,
    silhouette_mask,
    xor_image,
)


class TestSilhouetteMask(unittest.TestCase):
    """Both upstream (RGB + magic-pink) and ours (RGBA) classify
    pixels via the same helper; the test pins the convention against
    synthetic atlases."""

    def test_alpha_drives_mask_on_rgba(self):
        rgba = np.zeros((4, 4, 4), dtype=np.uint8)
        rgba[1:3, 1:3, 3] = 255
        m = silhouette_mask(rgba)
        self.assertEqual(m.sum(), 4)

    def test_magic_pink_excluded_even_at_full_alpha(self):
        # PIL .convert("RGBA") on a magic-pink RGB pixel emits
        # (231, 255, 255, 255) -- the mask must strip those out
        # despite alpha=255, or upstream's whole 128x128 cell
        # looks like silhouette.
        rgba = np.zeros((2, 2, 4), dtype=np.uint8)
        rgba[..., :3] = MAGIC_PINK
        rgba[..., 3] = 255
        rgba[0, 0, :3] = (12, 34, 56)
        m = silhouette_mask(rgba, magic_rgb=MAGIC_PINK)
        self.assertEqual(m.sum(), 1)
        self.assertTrue(m[0, 0])

    def test_alpha_threshold_drops_edge_aa(self):
        # Vehicles & trees calibrate at >16 to drop EEVEE/Cycles edge
        # AA; buildings & fence at >0 to keep it.  Pin both branches.
        rgba = np.zeros((1, 3, 4), dtype=np.uint8)
        rgba[0, 0, 3] = 8   # below 16
        rgba[0, 1, 3] = 32  # above 16
        rgba[0, 2, 3] = 255
        self.assertEqual(silhouette_mask(rgba, alpha_threshold=0).sum(), 3)
        self.assertEqual(silhouette_mask(rgba, alpha_threshold=16).sum(), 2)

    def test_rgb_input_relies_on_magic_pink(self):
        # Upstream grounds & fence PNGs are RGB-only -- alpha threshold
        # is moot, magic_rgb is the only discriminator.
        rgb = np.zeros((2, 2, 3), dtype=np.uint8)
        rgb[:, :] = MAGIC_PINK
        rgb[0, 0] = (10, 20, 30)
        m = silhouette_mask(rgb, magic_rgb=MAGIC_PINK)
        self.assertEqual(m.sum(), 1)
        self.assertTrue(m[0, 0])


class TestIoU(unittest.TestCase):
    def test_full_match(self):
        m = np.array([[True, True], [True, False]])
        self.assertEqual(iou(m, m), 1.0)

    def test_disjoint(self):
        a = np.array([[True, False], [False, False]])
        b = np.array([[False, True], [False, False]])
        self.assertEqual(iou(a, b), 0.0)

    def test_empty_union_returns_zero(self):
        # An empty render reports failure rather than a perfect match;
        # the mathematical "two empty masks are identical" answer would
        # mask exactly the bug we want IoU to surface.
        z = np.zeros((4, 4), dtype=bool)
        self.assertEqual(iou(z, z), 0.0)


class TestDRGB(unittest.TestCase):
    def test_mean_abs_delta_over_all_pixels_common_bg(self):
        # Two 2x2 RGBA cells, composited onto MAGIC_PINK (231, 255, 255):
        # - (0,0): both in mask; delta = (10, 20, 30), |sum| = 60
        # - (0,1): ours-only -> ours (200,200,200) vs pink (231,255,255);
        #          per-channel |31, 55, 55|, |sum| = 141
        # - (1,0): upstream-only -> pink vs (200,200,200); same |sum| = 141
        # - (1,1): both transparent -> both pink, delta = 0
        # Mean over 4 pixels * 3 channels = (60 + 141 + 141 + 0) / 12 = 28.5
        a = np.zeros((2, 2, 4), dtype=np.uint8)
        b = np.zeros((2, 2, 4), dtype=np.uint8)
        am = np.zeros((2, 2), dtype=bool)
        bm = np.zeros((2, 2), dtype=bool)
        a[0, 0, :3] = (100, 100, 100); am[0, 0] = True
        b[0, 0, :3] = (110, 120, 130); bm[0, 0] = True
        a[0, 1, :3] = (200, 200, 200); am[0, 1] = True
        b[1, 0, :3] = (200, 200, 200); bm[1, 0] = True
        self.assertAlmostEqual(drgb_intersection(a, b, am, bm), 28.5)

    def test_nan_when_both_masks_empty(self):
        z = np.zeros((2, 2, 4), dtype=np.uint8)
        m = np.zeros((2, 2), dtype=bool)
        self.assertTrue(math.isnan(drgb_intersection(z, z, m, m)))


class TestXORImage(unittest.TestCase):
    def test_three_colour_regions(self):
        a = np.array([[True, True, False, False]])
        b = np.array([[True, False, True, False]])
        img = xor_image(a, b)
        # (red, blue, grey, transparent) per definition.
        self.assertEqual(img.shape, (1, 4, 4))
        np.testing.assert_array_equal(img[0, 0], (180, 180, 180, 255))  # both
        np.testing.assert_array_equal(img[0, 1], (230, 60, 60, 255))    # a only
        np.testing.assert_array_equal(img[0, 2], (60, 90, 230, 255))    # b only
        np.testing.assert_array_equal(img[0, 3], (0, 0, 0, 0))          # neither


class TestCellMetric(unittest.TestCase):
    def test_returns_metric_and_both_masks(self):
        # 4x4 RGBA: identical opaque 2x2 patch at (1:3, 1:3); rest transparent.
        a = np.zeros((4, 4, 4), dtype=np.uint8)
        a[1:3, 1:3] = (10, 20, 30, 255)
        b = a.copy()
        m, am, bm = cell_metric(a, b)
        self.assertEqual(m.iou, 1.0)
        self.assertEqual(m.xor_px, 0)
        self.assertEqual(am.shape, (4, 4))
        self.assertEqual(am.sum(), 4)
        np.testing.assert_array_equal(am, bm)


class TestComposeGrid(unittest.TestCase):
    """`compose_grid` is geometry-heavy (cell-count → image dims); pin
    the shape so silent drift in a future kwarg/loop edit is caught."""

    def _cell(self):
        rgba = np.zeros((128, 128, 4), dtype=np.uint8)
        rgba[16:48, 16:48] = (200, 100, 50, 255)
        mask = silhouette_mask(rgba)
        return GridCell(rgba, rgba, mask, mask, "x")

    def test_image_dims_match_cell_count(self):
        cells = [self._cell() for _ in range(3)]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "grid.png"
            compose_grid(cells, out_path=out)
            with Image.open(out) as img:
                # cell_px=128, pad=8, label_h=18 →
                #   w = 3*(128+8) + 8 = 416
                #   h = 3*(128+8) + 8 + 18 = 434
                self.assertEqual(img.size, (416, 434))

    def test_strip_magic_rgb_does_not_mutate_caller_array(self):
        # Buildings pass MAGIC_PINK to strip the keyed pixels before paste;
        # the caller's array must not get clobbered (they reuse it elsewhere).
        rgba = np.zeros((128, 128, 4), dtype=np.uint8)
        rgba[..., :3] = MAGIC_PINK
        rgba[..., 3] = 255
        original = rgba.copy()
        cell = GridCell(rgba, rgba, np.zeros((128, 128), bool),
                        np.zeros((128, 128), bool), "x")
        with tempfile.TemporaryDirectory() as tmp:
            compose_grid([cell], out_path=Path(tmp) / "g.png",
                         strip_magic_rgb=MAGIC_PINK)
        np.testing.assert_array_equal(rgba, original)


if __name__ == "__main__":
    unittest.main()
