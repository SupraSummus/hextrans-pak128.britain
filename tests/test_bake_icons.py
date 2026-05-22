"""Tests for `pak.bake_icons`.

`_parse` pins the dat-format contract; `_compose_atlas` pins the
cell-coord→pixel math.  Network-bound `slice_for` is exercised
end-to-end by `make bake-icons` under the rebake CI job.
"""

from __future__ import annotations

import unittest

from PIL import Image

from pak.bake_icons import CELL_PX, _CellRef, _compose_atlas, _parse


class TestParseCellRef(unittest.TestCase):
    def test_arrow_form_stripped(self):
        c = _parse("./images/foo.3.4")
        self.assertEqual((c.stem, c.row, c.col), ("images/foo", 3, 4))

    def test_bare_stem(self):
        c = _parse("foo.0.0")
        self.assertEqual((c.stem, c.row, c.col), ("foo", 0, 0))

    def test_rejects_no_coords(self):
        with self.assertRaisesRegex(ValueError, "bad cell ref"):
            _parse("./images/foo")


class TestComposeAtlas(unittest.TestCase):
    def test_lays_cells_left_to_right(self):
        # Build a 6×5-cell source where cells (3,4) and (3,5) carry
        # distinct colours; composing them in that order must place
        # the first at slot 0 and the second at slot 1.
        n = CELL_PX
        src = Image.new("RGBA", (6 * n, 5 * n))
        src.paste((255, 0, 0, 255), (4 * n, 3 * n, 5 * n, 4 * n))  # (3,4)
        src.paste((0, 0, 255, 255), (5 * n, 3 * n, 6 * n, 4 * n))  # (3,5)

        out = _compose_atlas(src, [_CellRef("foo", 3, 4), _CellRef("foo", 3, 5)])

        self.assertEqual(out.size, (2 * n, n))
        self.assertEqual(out.getpixel((0, 0)), (255, 0, 0, 255))
        self.assertEqual(out.getpixel((n, 0)), (0, 0, 255, 255))

    def test_single_cell(self):
        n = CELL_PX
        src = Image.new("RGBA", (n, n), (123, 45, 67, 255))
        out = _compose_atlas(src, [_CellRef("foo", 0, 0)])
        self.assertEqual(out.size, (n, n))
        self.assertEqual(out.getpixel((0, 0)), (123, 45, 67, 255))


if __name__ == "__main__":
    unittest.main()
