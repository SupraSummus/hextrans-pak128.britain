"""Structural shape check on each way SPEC's `materials=` dict.

Catches malformed RGB entries (wrong arity, non-int, out-of-range)
without invoking Blender.  Material-name correctness is left to the
bake driver, which raises `RuntimeError: --materials targets unknown
blend materials: [...]` when a key doesn't match the open blend's
slot set -- duplicating that check here would force every new blend
to maintain a slot-set table here in lockstep, with the blend itself
as the actual source of truth.
"""
from __future__ import annotations

import importlib
import unittest
from types import ModuleType

from pak import REPO_ROOT


def _ways_specs_with_materials() -> list[tuple[str, ModuleType]]:
    out: list[tuple[str, ModuleType]] = []
    for path in sorted((REPO_ROOT / "ways").glob("*.py")):
        if path.name == "__init__.py":
            continue
        mod_name = f"ways.{path.stem}"
        mod = importlib.import_module(mod_name)
        spec = getattr(mod, "SPEC", None)
        if getattr(spec, "materials", None):
            out.append((mod_name, mod))
    return out


class TestWayScriptMaterials(unittest.TestCase):

    def test_at_least_one_script_exists(self):
        # Guard against an "all materials got deleted" silent pass.
        self.assertGreater(len(_ways_specs_with_materials()), 0)

    def test_every_materials_dict_is_well_formed(self):
        for name, mod in _ways_specs_with_materials():
            with self.subTest(script=name):
                materials = mod.SPEC.materials
                self.assertIsInstance(materials, dict)
                for material, rgb in materials.items():
                    self.assertIsInstance(material, str)
                    self.assertEqual(len(rgb), 3,
                                     f"{name}.SPEC.materials[{material!r}] "
                                     "isn't a 3-tuple")
                    for ch in rgb:
                        self.assertIsInstance(ch, int)
                        self.assertGreaterEqual(ch, 0)
                        self.assertLessEqual(ch, 255)


if __name__ == "__main__":
    unittest.main()
