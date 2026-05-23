"""Property tests for `pak.sq_split` (port of An-dz/tilecutter).

Two complementary fixtures:

  * `tests/data/simutrans_wiki_cut.png` -- the schematic from the
    Simutrans wiki's GraphicsCutting page (paksize 64, 3×3×2
    footprint).  Property: cut, then stitch -- pixels claimed by
    some cell's mask must roundtrip; cells must not double-claim.
    Self-consistency check on the mask-set + corner rules.

  * `tests/data/oil-refinery.png` + `industry/oil-refinery.dat`
    (OilRefinery1955, largest upstream multi-tile, multi-height
    asset).  Property: stitch upstream cells, cut the canvas, output
    matches upstream pixel-exact.  Pins that the algorithm matches
    the cuts pak128.Britain's artists actually shipped.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from pak import dat as _dat
from pak.sq_split import MAGIC_PINK, W, cell_anchors, claim_mask, split, stitch

_REPO_ROOT = Path(__file__).resolve().parent.parent
_REFINERY_DAT = _REPO_ROOT / "industry" / "oil-refinery.dat"
_REFINERY_ATLAS = _REPO_ROOT / "tests" / "data" / "oil-refinery.png"
_REFINERY_NAME = "OilRefinery1955"
_WIKI_PNG = _REPO_ROOT / "tests" / "data" / "simutrans_wiki_cut.png"


def _non_pink(arr: np.ndarray) -> np.ndarray:
    return (arr[..., :3] != MAGIC_PINK).any(axis=-1)


def _load_upstream_refinery_cells(layout: int, season: int):
    obj = next(o for o in _dat.parse(_REFINERY_DAT)
               if any(k.lower() == "name" and v == _REFINERY_NAME
                      for k, v in o))
    atlas = np.asarray(Image.open(_REFINERY_ATLAS).convert("RGBA"))
    cells: dict[tuple[int, int, int], np.ndarray] = {}
    for ref in _dat.iter_image_refs(obj, family="backimage"):
        if ref.row is None:
            continue
        L, y, x, h, _phase, s = (int(i) for i in ref.indices)
        if L != layout or s != season:
            continue
        cells[(y, x, h)] = atlas[ref.row * W:(ref.row + 1) * W,
                                 ref.col * W:(ref.col + 1) * W].copy()
    return cells


class TestSplitStitchRoundtripWiki(unittest.TestCase):
    DIMS_X = 3
    DIMS_Y = 3
    HEIGHTS = 2
    PAKSIZE = 64

    def test_roundtrip(self):
        canvas = np.asarray(Image.open(_WIKI_PNG).convert("RGBA"))
        keys = [(y, x, h)
                for h in range(self.HEIGHTS)
                for y in range(self.DIMS_Y)
                for x in range(self.DIMS_X)]
        anchors = cell_anchors(keys, paksize=self.PAKSIZE)
        # Shift anchors into the wiki canvas frame.
        ax0 = W // 2 * self.PAKSIZE // W
        ay0 = (3 * W // 4) * self.PAKSIZE // W
        sx = -min(a[0] - ax0 for a in anchors.values())
        sy = -min(a[1] - ay0 for a in anchors.values())
        anchors = {k: (a[0] + sx, a[1] + sy) for k, a in anchors.items()}

        cells = split(canvas, anchors, paksize=self.PAKSIZE)
        reassembled = np.full_like(canvas, 255)
        reassembled[..., :3] = MAGIC_PINK
        stitch(cells, anchors, into_canvas=reassembled, paksize=self.PAKSIZE)

        claim = claim_mask(cells, anchors, canvas.shape, paksize=self.PAKSIZE)
        any_claim = claim > 0
        diff = (canvas[..., :3] != reassembled[..., :3]).any(axis=-1)
        self.assertEqual(
            int((diff & any_claim).sum()), 0,
            "cut->stitch roundtrip lost pixels in the mask-claimed region",
        )
        self.assertEqual(
            int((claim > 1).sum()), 0,
            "TileCutter masks overlap -- partition not disjoint",
        )


class TestStitchSplitRefinery(unittest.TestCase):
    def _check_layout(self, layout: int):
        upstream = _load_upstream_refinery_cells(layout, season=0)
        self.assertGreater(len(upstream), 0, f"L={layout}: no cells")

        canvas, anchors = stitch(upstream, cell_anchors(upstream.keys()))
        produced = split(canvas, anchors)

        claim = claim_mask(produced, anchors, canvas.shape)
        canvas_non_pink = _non_pink(canvas)
        total = int(canvas_non_pink.sum())
        lost = int((canvas_non_pink & (claim == 0)).sum())
        double = int(((claim > 1) & canvas_non_pink).sum())
        self.assertEqual(
            lost, 0,
            f"L={layout}: {lost}/{total} pixels not claimed by any cell",
        )
        self.assertEqual(
            double, 0,
            f"L={layout}: {double} pixels claimed by >1 cell",
        )

        # Cell-for-cell pixel-exact match against upstream art -- the
        # strictly-stronger property that pins our cuts to the ones
        # pak128.Britain's artists actually shipped.
        mismatched = [k for k, up in upstream.items()
                      if not np.array_equal(produced[k], up)]
        self.assertEqual(
            mismatched, [],
            f"L={layout}: {len(mismatched)} cells differ from upstream "
            f"(first 5: {mismatched[:5]})",
        )

    def test_layout_0(self):
        self._check_layout(0)

    def test_layout_1(self):
        self._check_layout(1)

    def test_layout_2(self):
        self._check_layout(2)

    def test_layout_3(self):
        self._check_layout(3)


if __name__ == "__main__":
    unittest.main()
