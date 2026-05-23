"""Property tests for `pak.hex_split` -- the hex counterpart to
`tests/test_sq_split.py`.

Synthetic 3-cell triangular footprint `(0,0), (1,0), (0,1)`,
painted with distinct per-cell colours, stitched onto a canvas, cut
back via `split`:

  * `test_roundtrip` -- cut->stitch identity on mask-claimed pixels.
    Covers anchor / stitch / cut coordinate-frame agreement.
  * `test_partition_disjoint` -- no canvas pixel claimed by more
    than one cell (`claim_mask <= 1`).

The square wiki test's "each cell is red xor blue" check doesn't
port: the wiki PNG is independent ground truth (hand-authored by
Simutrans contributors, not built around the cutter), but any
synthetic hex fixture is built knowing the cutter's geometry and
the check becomes tautological.
"""

from __future__ import annotations

import unittest

import numpy as np

from pak.cell_split import MAGIC_PINK
from pak.hex_split import DEFAULT_W, cell_anchors, claim_mask, split, stitch

_CELLS: list[tuple[int, int, int]] = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
_COLOURS: list[np.ndarray] = [
    np.array([255, 0, 0], dtype=np.uint8),
    np.array([0, 0, 255], dtype=np.uint8),
    np.array([0, 255, 0], dtype=np.uint8),
]


def _painted_cells() -> dict[tuple[int, int, int], np.ndarray]:
    """Per-cell `(W, W, 4)` sprite painted solid in the cell's colour."""
    out: dict[tuple[int, int, int], np.ndarray] = {}
    for k, colour in zip(_CELLS, _COLOURS, strict=True):
        sprite = np.empty((DEFAULT_W, DEFAULT_W, 4), dtype=np.uint8)
        sprite[..., :3] = colour
        sprite[..., 3] = 255
        out[k] = sprite
    return out


class TestHexSplitStitchRoundtrip(unittest.TestCase):

    def setUp(self):
        self.painted = _painted_cells()
        self.canvas, self.anchors = stitch(self.painted,
                                           cell_anchors(_CELLS))
        self.cut = split(self.canvas, self.anchors)

    def test_roundtrip(self):
        reassembled = np.empty_like(self.canvas)
        reassembled[..., :3] = MAGIC_PINK
        reassembled[..., 3] = 255
        stitch(self.cut, self.anchors, into_canvas=reassembled)
        claim = claim_mask(self.cut, self.anchors, self.canvas.shape)
        any_claim = claim > 0
        diff = (self.canvas[..., :3] != reassembled[..., :3]).any(axis=-1)
        self.assertEqual(
            int((diff & any_claim).sum()), 0,
            "cut->stitch roundtrip lost pixels in the mask-claimed region",
        )

    def test_partition_disjoint(self):
        claim = claim_mask(self.cut, self.anchors, self.canvas.shape)
        double = int((claim > 1).sum())
        self.assertEqual(
            double, 0,
            f"{double} pixels claimed by >1 cell -- partition not disjoint",
        )


if __name__ == "__main__":
    unittest.main()
