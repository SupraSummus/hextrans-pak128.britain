"""Every ported asset's committed `.dat` must match `emit_vehicle(SPEC)`.

A bake script (`<dir>/<basename>.py`) declaring a module-level
`SPEC: Vehicle` is the single source of truth for the dat; the
committed `<dir>/<basename>.dat` is its serialised output.  This
test re-runs `emit_vehicle` on every such SPEC and asserts
byte-identical against disk, so SPEC <-> dat drift fails CI on the
push that introduces it.

Cheap: pure-Python, no Blender, no PNG read.  PNG drift needs
the separate full rebake (see TODO.md -> "Vehicle rebake in CI").
"""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.threed.dat import emit_vehicle


_REPO = Path(__file__).resolve().parents[1]
_BAKE_DIRS = ("air", "trains", "trams")


def _ported_bake_scripts() -> list[Path]:
    """Per-asset bake scripts (`.py` with a sibling `.dat` and `.png`)."""
    scripts = []
    for d in _BAKE_DIRS:
        for py in sorted((_REPO / d).glob("*.py")):
            if py.stem == "__init__":
                continue
            if (py.with_suffix(".dat")).exists() and (py.with_suffix(".png")).exists():
                scripts.append(py)
    return scripts


class TestPortedDats(unittest.TestCase):

    def test_every_port_has_at_least_one(self):
        # Sanity that we're actually exercising something; if all ports
        # get deleted in a refactor, this test would silently pass.
        self.assertGreater(len(_ported_bake_scripts()), 0)

    def test_emit_matches_committed_dat(self):
        for script in _ported_bake_scripts():
            with self.subTest(script=script.relative_to(_REPO)):
                mod_name = f"{script.parent.name}.{script.stem}"
                mod = importlib.import_module(mod_name)
                spec = getattr(mod, "SPEC", None)
                if spec is None:
                    self.skipTest(f"{mod_name} has no SPEC (multi-object?)")
                with TemporaryDirectory() as d:
                    emitted = emit_vehicle(spec, out_dir=Path(d), basename=script.stem)
                    self.assertEqual(
                        emitted.read_text(),
                        script.with_suffix(".dat").read_text(),
                        f"{script.stem}.dat drift: re-run `python3 -m {mod_name}`",
                    )
