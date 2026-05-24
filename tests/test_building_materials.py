"""Structural shape checks on each building SPEC's `materials=` dict,
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
import json
import unittest
from types import ModuleType

import numpy as np

from pak import REPO_ROOT
from pak.materials import Lighting, Material, Slot, from_jsonable, seed_python, to_jsonable
from pak.tune_materials import proposed_color


def _spec_materials(spec) -> dict | None:
    """Read the materials dict from `spec.materials` or, on migrated
    scripts, from `spec.sprites.materials`.  See `pak.sprites` for
    the dual-shape transition; the consumer-tool migration TODO
    consolidates these accesses behind a single helper in `pak.bake`."""
    if getattr(spec, "materials", None):
        return spec.materials
    sprites = getattr(spec, "sprites", None)
    return getattr(sprites, "materials", None)


def _building_specs_with_materials() -> list[tuple[str, ModuleType]]:
    out: list[tuple[str, ModuleType]] = []
    for path in sorted((REPO_ROOT / "citybuildings").glob("*.py")):
        if path.name == "__init__.py":
            continue
        mod = importlib.import_module(f"citybuildings.{path.stem}")
        spec = getattr(mod, "SPEC", None)
        if _spec_materials(spec):
            out.append((path.stem, mod))
    return out


class TestBuildingScriptMaterials(unittest.TestCase):

    def test_at_least_one_script_exists(self):
        # Guard against an "all materials got deleted" silent pass.
        self.assertGreater(len(_building_specs_with_materials()), 0)

    def test_every_materials_dict_is_well_formed(self):
        for name, mod in _building_specs_with_materials():
            with self.subTest(script=name):
                materials = _spec_materials(mod.SPEC)
                self.assertIsInstance(materials, dict)
                for k, v in materials.items():
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

    def test_accepts_slots(self):
        Material(slots=[Slot(image="brick"), Slot(procedural="CLOUDS")])

    def test_rejects_slots_with_image(self):
        with self.assertRaisesRegex(ValueError, "cannot combine"):
            Material(slots=[Slot(image="brick")], image="brick")


class TestSlotConstructor(unittest.TestCase):

    def test_rejects_empty(self):
        with self.assertRaisesRegex(ValueError, "exactly one of"):
            Slot()

    def test_rejects_both_image_and_procedural(self):
        with self.assertRaisesRegex(ValueError, "exactly one of"):
            Slot(image="brick", procedural="CLOUDS")

    def test_rejects_unknown_procedural(self):
        with self.assertRaisesRegex(ValueError, "unknown procedural"):
            Slot(procedural="HOLLY")

    def test_rejects_unknown_blend(self):
        with self.assertRaisesRegex(ValueError, "unknown blend"):
            Slot(image="brick", blend="LERP")

    def test_accepts_image_slot(self):
        Slot(image="brick", texco="ORCO", size=(2.0, 2.0, 1.0))

    def test_accepts_procedural_slot(self):
        Slot(procedural="CLOUDS", fac=0.5)


class TestJsonRoundTrip(unittest.TestCase):

    def _sample(self):
        return {
            "Brick": Material(image="brick", size=(2.0, 2.0, 2.0)),
            "Roof":  Material(image="roof", texco="ORCO",
                              size=(3.0, 1.0, 2.0), ofs=(0.0, 0.02, 0.0)),
            "Hedge": Material(noise=True),
            "Tint":  Material(noise=True, color=(0.5, 0.8, 0.3)),
            "Stack": Material(slots=[
                Slot(image="brick", size=(4.0, 4.0, 1.0)),
                Slot(image="brick", texco="ORCO"),
                Slot(procedural="CLOUDS", blend="ADD", fac=0.7,
                     color=(0.1, 0.06, 0.04)),
            ]),
            "Band":  Material(slots=[
                Slot(procedural="CLOUDS", color_band=[
                    (0.0, 0.0, 0.0, 0.0, 0.0),
                    (1.0, 0.2, 0.4, 0.1, 1.0),
                ]),
            ]),
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

    def test_wire_form_omits_slot_defaults(self):
        # A slot at its full defaults still needs `image=` or
        # `procedural=` to construct; check the wire form drops the
        # other field-level defaults.
        wire = to_jsonable({"X": Material(slots=[Slot(image="brick")])})
        self.assertEqual(wire, {"X": {"slots": [{"image": "brick"}]}})

    def test_seed_python_is_executable(self):
        # `seed_python` output is meant for paste into a bake script;
        # exec it in a namespace where `Material` resolves and check
        # the resulting MATERIALS dict equals the input.
        mats = self._sample()
        src = seed_python(mats)
        ns: dict = {"Material": Material, "Slot": Slot}
        exec(src, ns)
        self.assertEqual(ns["MATERIALS"], mats)


class TestLighting(unittest.TestCase):

    def test_empty_lighting_is_all_none(self):
        # Every field defaults to None so a `Lighting()` block carries
        # no overrides -- the renderer falls back to globals.  The
        # wire form drops them all.
        self.assertEqual(Lighting().to_jsonable(), {})

    def test_jsonable_drops_none_fields(self):
        # Only set fields ride through the subprocess command line;
        # None means "fall back to global" and shouldn't override.
        L = Lighting(world_ambient=(0.55, 0.55, 0.55), sun_elev_deg=45.0)
        wire = L.to_jsonable()
        self.assertEqual(set(wire), {"world_ambient", "sun_elev_deg"})
        self.assertEqual(wire["world_ambient"], (0.55, 0.55, 0.55))
        self.assertEqual(wire["sun_elev_deg"], 45.0)

    def test_round_trip_preserves_tuples(self):
        # JSON turns tuples into lists; from_jsonable must re-tuple
        # the RGB triplet so equality with in-process Lighting holds.
        L = Lighting(world_ambient=(0.55, 0.55, 0.55),
                     sun_energy_scale=71.4,
                     sun_elev_deg=45.0, sun_az_offset_deg=-90.0)
        self.assertEqual(
            Lighting.from_jsonable(json.loads(json.dumps(L.to_jsonable()))),
            L,
        )


class TestProposedColor(unittest.TestCase):
    """`pak.tune_materials.proposed_color` is pure numpy.  The
    iterative loop driving it needs Blender, but the per-step solver
    is testable without one."""

    def test_pushes_toward_target(self):
        # Current declared (1,1,1), ours renders (100,100,100),
        # target upstream (200,100,100) -- R should scale up.
        new = proposed_color((1.0, 1.0, 1.0),
                             np.array([100, 100, 100]),
                             np.array([200, 100, 100]),
                             damping=1.0)
        self.assertGreater(new[0], 1.5)  # R nudged up
        self.assertAlmostEqual(new[1], 1.0, places=2)
        self.assertAlmostEqual(new[2], 1.0, places=2)

    def test_damping_shrinks_step(self):
        ours = np.array([100, 100, 100])
        up = np.array([200, 100, 100])
        aggressive = proposed_color((1.0,) * 3, ours, up, damping=1.0)
        timid = proposed_color((1.0,) * 3, ours, up, damping=0.2)
        # Timid step lands closer to the no-change point (1.0).
        self.assertLess(abs(timid[0] - 1.0), abs(aggressive[0] - 1.0))

    def test_gain_clamp_bounds_runaway(self):
        # Ours near-zero -- raw gain would be huge; clamp protects.
        new = proposed_color((1.0, 1.0, 1.0),
                             np.array([1, 1, 1]),
                             np.array([200, 200, 200]),
                             damping=1.0, gain_clamp=(0.5, 2.0))
        for c in new:
            self.assertLessEqual(c, 2.0)


if __name__ == "__main__":
    unittest.main()
