"""Structural checks on `MATERIALS` dicts in `ways/<rail>.py` bake scripts.

`pak/bake_way.py --materials <JSON>` reads the dict at bake time; a
malformed entry only fails when that variant is actually baked.
This runs on every push so the missing-key / out-of-range bug
breaks CI immediately, without waiting for the next Blender
invocation.  We walk `ways/*.py` directly rather than reusing
`pak.bake_units.discover` (which gates on `.dat` + `.png`
siblings) — an unbaked rail-script port is exactly the state we
want covered.
"""
from __future__ import annotations

import importlib
import unittest
from types import ModuleType

from pak import REPO_ROOT


_RAIL_MATERIALS: frozenset[str] = frozenset({"Ballast", "Wood", "Rail", "RailTop"})


def _ways_modules_with_materials() -> list[tuple[str, ModuleType]]:
    """Every `ways/<name>` module that exposes a top-level `MATERIALS`.

    Import-and-filter rather than text-grep: a comment mentioning
    `MATERIALS` would survive a grep, but `getattr` only returns the
    real binding.
    """
    out: list[tuple[str, ModuleType]] = []
    for path in sorted((REPO_ROOT / "ways").glob("*.py")):
        if path.name == "__init__.py":
            continue
        mod_name = f"ways.{path.stem}"
        mod = importlib.import_module(mod_name)
        if hasattr(mod, "MATERIALS"):
            out.append((mod_name, mod))
    return out


class TestRailScriptMaterials(unittest.TestCase):

    def test_at_least_one_rail_script_exists(self):
        # Guard against an "all rails got deleted" silent pass.
        self.assertGreater(len(_ways_modules_with_materials()), 0)

    def test_every_rail_script_has_well_formed_materials(self):
        for name, mod in _ways_modules_with_materials():
            with self.subTest(script=name):
                materials = mod.MATERIALS
                self.assertIsInstance(materials, dict)
                self.assertEqual(set(materials), _RAIL_MATERIALS,
                                 f"{name} MATERIALS keys don't match "
                                 "ns-cssr.blend's material slots")
                for material, rgb in materials.items():
                    self.assertEqual(len(rgb), 3,
                                     f"{name}.MATERIALS[{material!r}] "
                                     "isn't a 3-tuple")
                    for ch in rgb:
                        self.assertIsInstance(ch, int)
                        self.assertGreaterEqual(ch, 0)
                        self.assertLessEqual(ch, 255)


if __name__ == "__main__":
    unittest.main()
