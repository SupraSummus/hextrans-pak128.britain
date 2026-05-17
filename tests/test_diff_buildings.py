"""Tests for `pak.diff_buildings` -- the building-specific calibration
logic (atlas slicing, IoU matrix, permutation discovery, summary
stats).

Shared mask/IoU primitives are tested in `tests/test_diff.py`.  The
Blender-driven render half is exercised end-to-end via `python3 -m
pak.check citybuildings/<asset>.py`.

Run from the repo root:

    python3 -m unittest tests.test_diff_buildings
"""

from __future__ import annotations

import unittest
from tempfile import NamedTemporaryFile

import numpy as np
from PIL import Image

from pak.diff_buildings import _best_permutation, _iou_matrix, _split_upstream, summarise


class TestSplitUpstream(unittest.TestCase):
    def test_splits_row_zero_into_n_layouts(self):
        # Build a 4x2 atlas of 128x128 cells: each col gets a
        # different R-band so we can verify column ordering, and
        # row 1 (winter) gets a different G-band that the slice
        # must skip.
        arr = np.zeros((256, 512, 3), dtype=np.uint8)
        for c in range(4):
            arr[:128, c * 128:(c + 1) * 128] = [c * 50, 0, 0]
            arr[128:, c * 128:(c + 1) * 128] = [0, c * 50, 0]
        with NamedTemporaryFile(suffix=".png", delete=False) as fp:
            Image.fromarray(arr, "RGB").save(fp.name)
            cells = _split_upstream(fp.name, layouts=4)

        self.assertEqual(len(cells), 4)
        for c, cell in enumerate(cells):
            self.assertEqual(cell.shape, (128, 128, 4))
            self.assertTrue((cell[..., 0] == c * 50).all())
            self.assertTrue((cell[..., 1] == 0).all())  # winter row excluded

    def test_rejects_atlas_too_narrow_for_requested_layouts(self):
        arr = np.zeros((128, 256, 3), dtype=np.uint8)
        with NamedTemporaryFile(suffix=".png", delete=False) as fp:
            Image.fromarray(arr, "RGB").save(fp.name)
            with self.assertRaisesRegex(SystemExit, "needs at least"):
                _split_upstream(fp.name, layouts=4)


class TestBestPermutation(unittest.TestCase):
    def test_identity_wins_for_diagonal_matrix(self):
        self.assertEqual(_best_permutation(np.eye(4)), [0, 1, 2, 3])

    def test_recovers_arbitrary_permutation(self):
        # Anti-diagonal: rows 0..3 best match cols 3..0.  Greedy
        # would have worked here too, but enumeration is also
        # provably optimal — pin the result against the contract.
        m = np.array([
            [0.1, 0.2, 0.3, 0.9],
            [0.2, 0.3, 0.9, 0.2],
            [0.3, 0.9, 0.2, 0.1],
            [0.9, 0.2, 0.1, 0.0],
        ])
        self.assertEqual(_best_permutation(m), [3, 2, 1, 0])

    def test_picks_higher_trace_over_local_max(self):
        # A greedy row-by-row pick would take row 0 → col 0 (0.95)
        # and then row 1 is forced onto col 1 or 2 (both 0.20),
        # giving trace 1.35.  The optimum picks row 0 → col 1
        # (0.94) and row 1 → col 0 (0.93), trace 1.87 -- pins that
        # `_best_permutation` is doing global enumeration, not
        # greedy.
        m = np.array([
            [0.95, 0.94, 0.20],
            [0.93, 0.20, 0.20],
            [0.20, 0.20, 0.20],
        ])
        self.assertEqual(_best_permutation(m), [1, 0, 2])


class TestSummarise(unittest.TestCase):
    def test_returns_worst_best_diag(self):
        mat = np.array([
            [0.90, 0.10, 0.20, 0.30],
            [0.10, 0.95, 0.20, 0.20],
            [0.20, 0.20, 0.80, 0.10],
            [0.20, 0.10, 0.20, 0.85],
        ])
        worst, best, diag = summarise(mat, perm=[0, 1, 2, 3])
        self.assertEqual(worst, 0.80)
        self.assertAlmostEqual(best, (0.90 + 0.95 + 0.80 + 0.85) / 4)
        self.assertAlmostEqual(diag, (0.90 + 0.95 + 0.80 + 0.85) / 4)

    def test_uses_perm_not_diagonal(self):
        mat = np.array([
            [0.10, 0.90],
            [0.85, 0.20],
        ])
        worst, best, diag = summarise(mat, perm=[1, 0])
        self.assertEqual(worst, 0.85)
        self.assertAlmostEqual(best, 0.875)
        self.assertAlmostEqual(diag, 0.15)


class TestIoUMatrix(unittest.TestCase):
    def test_diagonal_full_match_when_masks_paired(self):
        a = np.array([[True, False], [False, True]])
        b = np.array([[False, True], [True, False]])
        mat = _iou_matrix([a, b], [a, b])
        np.testing.assert_array_equal(mat, np.eye(2))


if __name__ == "__main__":
    unittest.main()
