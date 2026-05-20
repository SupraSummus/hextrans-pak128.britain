"""Tests for `pak.diff_tunnel._parse_tunnel_image_entries` -- the
upstream tunnel dat -> per-facing Back+Front cell-coord parser that
drives the calibration stitch.

Run from the repo root:

    python3 -m unittest tests.test_diff_tunnel
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from pak.diff_tunnel import _parse_tunnel_image_entries


def _write_dat(body: str) -> Path:
    fp = NamedTemporaryFile(suffix=".dat", delete=False, mode="w")
    fp.write(body)
    fp.close()
    return Path(fp.name)


class TestParseTunnelImageEntries(unittest.TestCase):
    def test_sparse_back_collapses_to_front_only(self):
        # Stone-tunnel shape: Front on all 4 facings, Back only on
        # W and N.  Facings with Front but no Back must still appear
        # in the result with `back=None` so the stitch falls back to
        # Front alone rather than skipping the facing.
        dat = _write_dat(
            "obj=tunnel\nName=x\n"
            "FrontImage[W][0]=stem.0.0\n"
            "BackImage[W][0]=stem.1.0\n"
            "FrontImage[N][0]=stem.0.1\n"
            "BackImage[N][0]=stem.1.1\n"
            "FrontImage[E][0]=stem.0.2\n"
            "FrontImage[S][0]=stem.0.3\n"
            "----------\n"
        )
        entries = _parse_tunnel_image_entries(dat, name="x")
        self.assertEqual(entries["W"], {"front": (0, 0), "back": (1, 0)})
        self.assertEqual(entries["N"], {"front": (0, 1), "back": (1, 1)})
        self.assertEqual(entries["E"], {"front": (0, 2), "back": None})
        self.assertEqual(entries["S"], {"front": (0, 3), "back": None})

    def test_filters_by_name_in_multi_object_dat(self):
        # tunnels.dat packs every variant into one file; the name
        # filter picks the requested object.  Without it, callers
        # would silently get the first object's atlas coords.
        dat = _write_dat(
            "obj=tunnel\nName=Stone\n"
            "FrontImage[N][0]=stone.0.1\n"
            "----------\n"
            "obj=tunnel\nName=Brick\n"
            "FrontImage[N][0]=brick.0.1\n"
            "----------\n"
        )
        stone = _parse_tunnel_image_entries(dat, name="Stone")
        self.assertEqual(stone["N"]["front"], (0, 1))
        # Case-insensitive name match -- upstream Name= casing varies.
        brick = _parse_tunnel_image_entries(dat, name="brick")
        self.assertEqual(brick["N"]["front"], (0, 1))
        with self.assertRaisesRegex(SystemExit, "no obj named 'Gamma'"):
            _parse_tunnel_image_entries(dat, name="Gamma")

    def test_preserves_facing_label_case(self):
        # The dat-side facing-label case has to round-trip so the
        # result keys match `SQUARE_FACING_LABELS` ("S"/"N"/"E"/"W").
        # A lowercased regex would dict-key by "s"/"n"/"e"/"w" and
        # break the lookup silently; this pins the regex.
        dat = _write_dat(
            "obj=tunnel\nName=x\n"
            "FrontImage[S][0]=stem.0.0\n"
            "frontimage[N][0]=stem.0.1\n"  # key tag mixed case
            "----------\n"
        )
        entries = _parse_tunnel_image_entries(dat, name="x")
        self.assertIn("S", entries)
        self.assertIn("N", entries)

    def test_ignores_unparseable_image_refs(self):
        dat = _write_dat(
            "obj=tunnel\nName=x\n"
            "FrontImage[N][0]=-\n"
            "FrontImage[S][0]=stem.0.3\n"
            "----------\n"
        )
        entries = _parse_tunnel_image_entries(dat, name="x")
        self.assertNotIn("N", entries)
        self.assertEqual(entries["S"]["front"], (0, 3))


if __name__ == "__main__":
    unittest.main()
