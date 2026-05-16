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

from pak.bake_units import discover, import_script, specs_of
from pak.dat import (
    Building, Vehicle, Way,
    emit_building, emit_vehicles, emit_way,
)


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
                    out_dir, basename = Path(d), script.stem
                    if all(isinstance(s, Vehicle) for s in specs):
                        emitted = emit_vehicles(specs, out_dir=out_dir, basename=basename)
                    elif len(specs) == 1 and isinstance(specs[0], Way):
                        emitted = emit_way(specs[0], out_dir=out_dir, basename=basename)
                    elif len(specs) == 1 and isinstance(specs[0], Building):
                        emitted = emit_building(specs[0], out_dir=out_dir, basename=basename)
                    else:
                        self.fail(f"{mod.__name__} has unsupported SPEC/SPECS shape")
                    self.assertEqual(
                        emitted.read_text(),
                        script.with_suffix(".dat").read_text(),
                        f"{script.stem}.dat drift: re-run `python3 -m {mod.__name__}`",
                    )
