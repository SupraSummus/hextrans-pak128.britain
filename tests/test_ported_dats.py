"""Every ported asset's committed `.dat` must match `emit_*(SPEC)`.

A bake script (`<dir>/<basename>.py`) declaring a module-level
`SPEC: Vehicle | Way` is the single source of truth for the dat;
the committed `<dir>/<basename>.dat` is its serialised output.
This test re-runs the matching emitter on every such SPEC and
asserts byte-identical against disk, so SPEC <-> dat drift fails
CI on the push that introduces it.

Cheap: pure-Python, no Blender, no PNG read.  PNG drift needs
the separate full rebake (see TODO.md -> "Vehicle rebake in CI").
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pak.bake import _BAKE_REGISTRY
from pak.bake_units import discover, import_script, specs_of
from pak.reemit_dats import emit_for_specs


class TestPortedDats(unittest.TestCase):

    def test_every_port_has_at_least_one(self):
        # Sanity that we're actually exercising something; if all ports
        # get deleted in a refactor, this test would silently pass.
        self.assertGreater(len(discover()), 0)

    def test_emit_matches_committed_dat(self):
        for script in discover():
            with self.subTest(script=script.name):
                mod = import_script(script)
                specs = specs_of(mod)
                self.assertTrue(specs, f"{mod.__name__} has no SPEC or SPECS")
                with TemporaryDirectory() as d:
                    emitted = emit_for_specs(specs, Path(d), script.stem)
                    self.assertEqual(
                        emitted.read_text(),
                        script.with_suffix(".dat").read_text(),
                        f"{script.stem}.dat drift: re-run `python3 -m {mod.__name__}`",
                    )

    def test_every_spec_type_is_bake_registered(self):
        # `bake_main` only runs locally on `python3 -m <script>`, so the
        # standard test pass and reemit lint won't surface a new SPEC type
        # whose bake function was added without a `_BAKE_REGISTRY` entry.
        # Pins the cross-asset invariant at push time instead of next-bake.
        for script in discover():
            with self.subTest(script=script.name):
                specs = specs_of(import_script(script))
                self.assertIn(type(specs[0]), _BAKE_REGISTRY)
