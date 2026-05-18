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

from pak.upstream import _first_image_ref, _strip_ref


def _write_dat(body: str) -> Path:
    fp = NamedTemporaryFile(suffix=".dat", delete=False, mode="w")
    fp.write(body)
    fp.close()
    return Path(fp.name)


class TestFirstImageRef(unittest.TestCase):
    def test_vehicle_emptyimage(self):
        dat = _write_dat(
            "obj=vehicle\nname=test\n"
            "EmptyImage[E][0]=./carriages/foo_E.0.0\n"
            "EmptyImage[S][0]=./carriages/foo_S.0.0\n"
            "----------\n"
        )
        self.assertEqual(
            _first_image_ref(dat, name=None),
            "./carriages/foo_E.0.0",
        )

    def test_building_backimage(self):
        dat = _write_dat(
            "obj=building\nName=BAR\n"
            "BackImage[0][0][0][0][0][0]=images/com/bar.0.0\n"
            "----------\n"
        )
        self.assertEqual(
            _first_image_ref(dat, name=None),
            "images/com/bar.0.0",
        )

    def test_tree_image(self):
        dat = _write_dat(
            "obj=tree\nname=test\n"
            "image[0][0]=./oak.0.0\n"
            "image[1][0]=./oak.0.1\n"
            "----------\n"
        )
        self.assertEqual(
            _first_image_ref(dat, name=None),
            "./oak.0.0",
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
            _first_image_ref(dat, name="BETA"),
            "images/beta.0.0",
        )
        # Name match is case-insensitive.
        self.assertEqual(
            _first_image_ref(dat, name="alpha"),
            "images/alpha.0.0",
        )

    def test_missing_name_raises(self):
        dat = _write_dat(
            "obj=building\nName=ALPHA\n"
            "BackImage[0][0][0][0][0][0]=images/alpha.0.0\n"
            "----------\n"
        )
        with self.assertRaisesRegex(SystemExit, "no obj named 'GAMMA'"):
            _first_image_ref(dat, name="GAMMA")

    def test_skips_non_image_keys(self):
        # `name=` happens to share a `=` shape with image refs but
        # the regex anchors on bracketed `…image[…]` keys, so name=
        # / Level= / class_proportion[N]= shouldn't match.
        dat = _write_dat(
            "obj=building\nName=X\nLevel=5\n"
            "class_proportion[0]=10\n"
            "BackImage[0][0][0][0][0][0]=images/x.0.0\n"
            "----------\n"
        )
        self.assertEqual(_first_image_ref(dat, name=None), "images/x.0.0")


class TestStripRef(unittest.TestCase):
    def test_vehicle_facing_and_rowcol(self):
        self.assertEqual(
            _strip_ref("./carriages/foo_E.0.0", PurePosixPath("trains")),
            "trains/carriages/foo",
        )

    def test_vehicle_with_offset_tail(self):
        # Upstream often appends a per-image x,y screen offset:
        # `./images/dogger_E.0.0,-33,14` — the comma tail must come
        # off before the suffix strips can match.
        self.assertEqual(
            _strip_ref("./images/dogger_E.0.0,-33,14", PurePosixPath("boats")),
            "boats/images/dogger",
        )

    def test_building_atlas_no_facing(self):
        self.assertEqual(
            _strip_ref("images/com/bar.0.0", PurePosixPath("citybuildings")),
            "citybuildings/images/com/bar",
        )

    def test_tree_bare_stem(self):
        self.assertEqual(
            _strip_ref("./oak.0.0", PurePosixPath("trees")),
            "trees/oak",
        )


if __name__ == "__main__":
    unittest.main()
