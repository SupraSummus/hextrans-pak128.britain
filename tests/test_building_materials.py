"""Structural shape checks on `MATERIALS` dicts in `citybuildings/<asset>.py`,
plus round-trip tests on `pak.materials`.

`Material.__post_init__` validates field shape (texco enum, image-xor-noise
mutual exclusion), so this file leans on the constructor instead of
redoing the checks.  Material-name correctness against the .blend's slot
set is left to the bake driver, which raises at render time when a key
doesn't match -- duplicating that check here would force every new
blend to maintain a slot-set table in lockstep with the blend itself,
which is the actual source of truth.  Mirrors `tests/test_way_materials.py`.
"""
from __future__ import annotations

import importlib
import unittest
from types import ModuleType

from pak import REPO_ROOT
from pak.materials import Material, from_jsonable, seed_python, to_jsonable


def _building_modules_with_materials() -> list[tuple[str, ModuleType]]:
    out: list[tuple[str, ModuleType]] = []
    for path in sorted((REPO_ROOT / "citybuildings").glob("*.py")):
        if path.name == "__init__.py":
            continue
        mod = importlib.import_module(f"citybuildings.{path.stem}")
        if hasattr(mod, "MATERIALS"):
            out.append((path.stem, mod))
    return out


class TestBuildingScriptMaterials(unittest.TestCase):

    def test_at_least_one_script_exists(self):
        # Guard against an "all MATERIALS got deleted" silent pass.
        self.assertGreater(len(_building_modules_with_materials()), 0)

    def test_every_materials_dict_is_well_formed(self):
        for name, mod in _building_modules_with_materials():
            with self.subTest(script=name):
                self.assertIsInstance(mod.MATERIALS, dict)
                for k, v in mod.MATERIALS.items():
                    self.assertIsInstance(k, str)
                    self.assertIsInstance(v, Material)


class TestMaterialConstructor(unittest.TestCase):

    def test_rejects_empty(self):
        with self.assertRaisesRegex(ValueError, "image=.*or noise=True"):
            Material()

    def test_rejects_image_and_noise(self):
        with self.assertRaisesRegex(ValueError, "cannot also be noise"):
            Material(image="foo", noise=True)

    def test_rejects_unknown_texco(self):
        with self.assertRaisesRegex(ValueError, "unknown texco"):
            Material(image="foo", texco="WORLD")

    def test_accepts_image(self):
        Material(image="brick", size=(2.0, 2.0, 2.0))

    def test_accepts_noise(self):
        Material(noise=True)


class TestJsonRoundTrip(unittest.TestCase):

    def _sample(self):
        return {
            "Brick": Material(image="brick", size=(2.0, 2.0, 2.0)),
            "Roof":  Material(image="roof", texco="ORCO",
                              size=(3.0, 1.0, 2.0), ofs=(0.0, 0.02, 0.0)),
            "Hedge": Material(noise=True),
        }

    def test_round_trip(self):
        mats = self._sample()
        self.assertEqual(from_jsonable(to_jsonable(mats)), mats)

    def test_wire_form_omits_default_fields(self):
        # Defaults are stable, so the wire form should be the shortest
        # representation that round-trips -- noise=True alone for Hedge,
        # nothing leaked through from the {texco, size, ofs} defaults.
        wire = to_jsonable({"Hedge": Material(noise=True)})
        self.assertEqual(wire, {"Hedge": {"noise": True}})

    def test_seed_python_is_executable(self):
        # `seed_python` output is meant for paste into a bake script;
        # exec it in a namespace where `Material` resolves and check
        # the resulting MATERIALS dict equals the input.
        mats = self._sample()
        src = seed_python(mats)
        ns: dict = {"Material": Material}
        exec(src, ns)
        self.assertEqual(ns["MATERIALS"], mats)


if __name__ == "__main__":
    unittest.main()
