"""Tests for `pak.upstream` -- image-stem derivation from upstream dats.

The network-touching `image_stem()` driver is exercised end-to-end via
`python3 -m pak.check`.  These tests pin the parse + strip primitives
against synthetic dats so the half that's pure code is checkable
without fetching upstream.
"""

from __future__ import annotations

import unittest
from pathlib import Path, PurePosixPath
from tempfile import NamedTemporaryFile

from pak.upstream import _first_image_basename, _resolve_stem


def _write_dat(body: str) -> Path:
    fp = NamedTemporaryFile(suffix=".dat", delete=False, mode="w")
    fp.write(body)
    fp.close()
    return Path(fp.name)


class TestFirstImageBasename(unittest.TestCase):
    def test_vehicle_emptyimage(self):
        dat = _write_dat(
            "obj=vehicle\nname=test\n"
            "EmptyImage[E][0]=./carriages/foo_E.0.0\n"
            "EmptyImage[S][0]=./carriages/foo_S.0.0\n"
            "----------\n"
        )
        self.assertEqual(
            _first_image_basename(dat, name=None),
            "./carriages/foo_E",
        )

    def test_vehicle_offset_tail_stripped(self):
        # Upstream often appends a per-image x,y screen offset:
        # `./images/dogger_E.0.0,-33,14`.  `iter_image_refs` already
        # peels the offset + atlas tail into `basename`, so
        # `_first_image_basename` doesn't see the comma tail.
        dat = _write_dat(
            "obj=vehicle\nname=test\n"
            "EmptyImage[E][0]=./images/dogger_E.0.0,-33,14\n"
            "----------\n"
        )
        self.assertEqual(
            _first_image_basename(dat, name=None),
            "./images/dogger_E",
        )

    def test_building_backimage(self):
        dat = _write_dat(
            "obj=building\nName=BAR\n"
            "BackImage[0][0][0][0][0][0]=images/com/bar.0.0\n"
            "----------\n"
        )
        self.assertEqual(
            _first_image_basename(dat, name=None),
            "images/com/bar",
        )

    def test_filters_by_name(self):
        dat = _write_dat(
            "obj=building\nName=ALPHA\n"
            "BackImage[0][0][0][0][0][0]=images/alpha.0.0\n"
            "----------\n"
            "obj=building\nName=BETA\n"
            "BackImage[0][0][0][0][0][0]=images/beta.0.0\n"
            "----------\n"
        )
        self.assertEqual(
            _first_image_basename(dat, name="BETA"), "images/beta",
        )
        # Name match is case-insensitive.
        self.assertEqual(
            _first_image_basename(dat, name="alpha"), "images/alpha",
        )

    def test_missing_name_raises(self):
        dat = _write_dat(
            "obj=building\nName=ALPHA\n"
            "BackImage[0][0][0][0][0][0]=images/alpha.0.0\n"
            "----------\n"
        )
        with self.assertRaisesRegex(SystemExit, "no obj named 'GAMMA'"):
            _first_image_basename(dat, name="GAMMA")

    def test_skips_non_image_keys(self):
        # `name=`, `Level=`, `class_proportion[N]=` aren't image-family
        # keys so the iterator skips them; the BackImage ref wins.
        dat = _write_dat(
            "obj=building\nName=X\nLevel=5\n"
            "class_proportion[0]=10\n"
            "BackImage[0][0][0][0][0][0]=images/x.0.0\n"
            "----------\n"
        )
        self.assertEqual(_first_image_basename(dat, name=None), "images/x")


class TestResolveStem(unittest.TestCase):
    def test_vehicle_facing(self):
        self.assertEqual(
            _resolve_stem("./carriages/foo_E", PurePosixPath("trains")),
            "trains/carriages/foo",
        )

    def test_building_no_facing(self):
        self.assertEqual(
            _resolve_stem("images/com/bar", PurePosixPath("citybuildings")),
            "citybuildings/images/com/bar",
        )

    def test_tree_bare_stem(self):
        self.assertEqual(
            _resolve_stem("./oak", PurePosixPath("trees")),
            "trees/oak",
        )


if __name__ == "__main__":
    unittest.main()
