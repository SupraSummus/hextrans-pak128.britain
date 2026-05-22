"""Tests for `pak.tune_industries.inject_into_script` -- the text
mangling that wires `MATERIALS` / `LIGHTING` into a bake script.  The
solver and rendering paths are integration-covered by running the
script; this test pins only the surface-level text shape that runtime
wouldn't catch with a useful error.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from pak.tune_industries import inject_into_script

BLOCK = """\
# AUTO-TUNED: pak.tune_industries
MATERIALS = {
    'X': Material(image='foo'),
}

LIGHTING = Lighting(world_ambient=(0.45, 0.45, 0.45))
# END AUTO-TUNED"""

SPECS_FORM = """\
from pak.bake import bake_factory_main
from pak.dat import Factory

SPECS = [
    Factory(
        name="A",
        blend="x.blend",
        upstream_dat="y.dat",
    ),
    Factory(
        name="B",
        blend="x.blend",
        upstream_dat="y.dat",
    ),
]
"""

SPEC_FORM = """\
from pak.bake import bake_factory_main
from pak.dat import Factory

SPEC = Factory(
    name="A",
    blend="x.blend",
    upstream_dat="y.dat",
)
"""


def _inject(source: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(source)
        path = Path(f.name)
    try:
        inject_into_script(path, BLOCK)
        return path.read_text()
    finally:
        path.unlink()


class TestInject(unittest.TestCase):

    def test_specs_list_form(self):
        out = _inject(SPECS_FORM)
        self.assertIn("from pak.materials import Lighting, Material", out)
        self.assertIn("MATERIALS = {", out)
        self.assertIn("LIGHTING = Lighting", out)
        # Each Factory gets materials=MATERIALS and lighting=LIGHTING wired.
        self.assertEqual(out.count("materials=MATERIALS,"), 2)
        self.assertEqual(out.count("lighting=LIGHTING,"), 2)

    def test_single_spec_form(self):
        out = _inject(SPEC_FORM)
        self.assertEqual(out.count("materials=MATERIALS,"), 1)
        self.assertEqual(out.count("lighting=LIGHTING,"), 1)

    def test_factory_kwarg_indent_matches_siblings(self):
        # SPECS-form: args indent at 8 spaces; the new kwarg should too.
        out = _inject(SPECS_FORM)
        self.assertIn("        materials=MATERIALS,", out)
        # SPEC-form: args indent at 4 spaces; closing `)` at column 0.
        out = _inject(SPEC_FORM)
        self.assertIn("    materials=MATERIALS,", out)
        self.assertNotIn("        materials=MATERIALS,", out)

    def test_idempotent(self):
        once = _inject(SPECS_FORM)
        twice = _inject(once)
        self.assertEqual(once, twice)
        self.assertEqual(twice.count("materials=MATERIALS,"), 2)
        # Only one AUTO-TUNED block survives a re-run.
        self.assertEqual(twice.count("# AUTO-TUNED: pak.tune_industries"), 1)


if __name__ == "__main__":
    unittest.main()
