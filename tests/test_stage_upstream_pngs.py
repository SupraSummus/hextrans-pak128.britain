"""Tests for `pak.stage_upstream_pngs.png_refs`.

The image-ref regex has to cover both flat single-bracket gui dats
(`Image[0]=construction-site.0.0`) and grounds layered double-bracket
refs (`Image[0][0]=images/fence-3.0.0`) — those are the two shapes
the staging pipeline feeds today.  No network: only the parse step
is exercised.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pak.stage_upstream_pngs import png_refs


def _write(d: Path, name: str, body: str) -> Path:
    p = d / name
    p.write_text(body)
    return p


class TestPngRefs(unittest.TestCase):

    def test_flat_single_bracket(self):
        with TemporaryDirectory() as d:
            dat = _write(Path(d), "x.dat", (
                "Obj=misc\nName=X\n"
                "Image[0]=construction-site.0.0\n"
                "Image[1]=construction-site.0.0\n"
            ))
            self.assertEqual(png_refs(dat), {"construction-site"})

    def test_layered_double_bracket_with_subpath(self):
        with TemporaryDirectory() as d:
            dat = _write(Path(d), "x.dat", (
                "Obj=ground\nName=X\n"
                "Image[0][0]=images/fence-3.0.0\n"
                "Image[1][0]=images/fence-4.0.0\n"
            ))
            self.assertEqual(png_refs(dat), {"images/fence-3", "images/fence-4"})

    def test_arrow_continuation_and_leading_dotslash(self):
        with TemporaryDirectory() as d:
            dat = _write(Path(d), "x.dat", (
                "Obj=misc\nName=X\n"
                "Image[0]=> big-logo-britain.0.0\n"
                "Image[1]=./big-logo-britain.0.1\n"
            ))
            self.assertEqual(png_refs(dat), {"big-logo-britain"})

    def test_optional_z_coord(self):
        with TemporaryDirectory() as d:
            dat = _write(Path(d), "x.dat", (
                "Obj=building\nName=X\n"
                "Image[0]=foo.0.0.0\n"
            ))
            self.assertEqual(png_refs(dat), {"foo"})

    def test_commented_and_non_image_lines_skipped(self):
        with TemporaryDirectory() as d:
            dat = _write(Path(d), "x.dat", (
                "Obj=misc\nName=X\n"
                "# Image[0]=ignored.0.0\n"
                "cursor=./real.0.0\n"
                "Image[0]=kept.0.0\n"
            ))
            self.assertEqual(png_refs(dat), {"kept"})


if __name__ == "__main__":
    unittest.main()
