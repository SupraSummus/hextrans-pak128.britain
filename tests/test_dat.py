"""Tests for `pak.dat`.

Run from the repo root:

    python3 -m pytest tests/

or, without pytest installed:

    python3 -m unittest tests.test_dat
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pak.dat import (
    Vehicle,
    emit_vehicle,
    parse,
    port_vehicle,
    seed_python,
)


SAMPLE_MULTI_OBJ = """\
# A header comment.
obj=vehicle
name=Foo
waytype=track
speed=100
----------
obj=vehicle
name=Bar
waytype=track
speed=80
----------
"""


class TestParse(unittest.TestCase):
    def test_splits_multi_object(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "x.dat"
            p.write_text(SAMPLE_MULTI_OBJ)
            objs = parse(p)
        self.assertEqual(len(objs), 2)
        self.assertEqual(dict(objs[0])["name"], "Foo")
        self.assertEqual(dict(objs[1])["name"], "Bar")

    def test_drops_blank_and_comments(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "x.dat"
            p.write_text("# top\nobj=vehicle\n\n  \nname=x\n# mid\n----------\n")
            (obj,) = parse(p)
        keys = [k for k, _ in obj]
        self.assertEqual(keys, ["obj", "name"])


class TestVehicleConstruction(unittest.TestCase):
    def test_rejects_unknown_kwarg(self):
        with self.assertRaisesRegex(TypeError, "unexpected keyword"):
            Vehicle(name="x", waytype="track", bogus_field=1)  # type: ignore[call-arg]

    def test_rejects_extended_misspelling(self):
        # Real field is `bidirectional`; typo must fail at construction.
        with self.assertRaisesRegex(TypeError, "unexpected keyword"):
            Vehicle(name="x", waytype="track", bidirecitonal=1)  # type: ignore[call-arg]

    def test_required_fields(self):
        with self.assertRaises(TypeError):
            Vehicle(name="x")  # missing waytype  # type: ignore[call-arg]


class TestEmitVehicle(unittest.TestCase):
    def _emit(self, v: Vehicle) -> str:
        with TemporaryDirectory() as d:
            emit_vehicle(v, out_dir=Path(d), basename="x")
            return (Path(d) / "x.dat").read_text()

    def test_minimal_skips_none(self):
        text = self._emit(Vehicle(name="A", waytype="track"))
        lines = text.splitlines()
        self.assertEqual(lines[0], "obj=vehicle")
        self.assertEqual(lines[1], "name=A")
        self.assertEqual(lines[2], "waytype=track")
        # No copyright / freight / etc. lines.
        body = lines[3:lines.index("EmptyImage[S]=./x.0.0")]  # row=0, col=0
        self.assertEqual(body, [])

    def test_emits_extended_fields(self):
        v = Vehicle(name="A", waytype="track", axles=4, comfort_by_class=[10, 20])
        text = self._emit(v)
        self.assertIn("axles=4\n", text)
        self.assertIn("comfort[0]=10\n", text)
        self.assertIn("comfort[1]=20\n", text)

    def test_scalar_comfort_emits_unindexed(self):
        text = self._emit(Vehicle(name="A", waytype="track", comfort=49))
        self.assertIn("comfort=49\n", text)
        self.assertNotIn("comfort[", text)

    def test_payload_by_class_uses_remapped_dat_key(self):
        v = Vehicle(name="A", waytype="track", payload_by_class=[0, 0, 0, 18])
        text = self._emit(v)
        self.assertIn("payload[3]=18\n", text)
        self.assertNotIn("payload_by_class", text)

    def test_constraint_uses_capitalised_form(self):
        v = Vehicle(name="A", waytype="track", constraint_next=["B", "C"])
        text = self._emit(v)
        self.assertIn("Constraint[Next][0]=B\n", text)
        self.assertIn("Constraint[Next][1]=C\n", text)

    def test_emits_eight_facing_image_refs(self):
        # makeobj parses `<file>.X.Y` as row=X, col=Y, so the single-row
        # hex atlas's 8 facings address as `.0.0` .. `.0.7`.
        text = self._emit(Vehicle(name="A", waytype="track"))
        for col, facing in enumerate(("S", "SW", "W", "NW", "N", "NE", "E", "SE")):
            self.assertIn(f"EmptyImage[{facing}]=./x.0.{col}\n", text)


class TestPortVehicle(unittest.TestCase):
    def test_round_trips_through_seed_python(self):
        original = Vehicle(
            name="X",
            waytype="track",
            speed=120,
            weight=12.5,
            payload=42,
            comfort_by_class=[1, 2, 3],
            constraint_prev=["any"],
        )
        # Render -> parse the resulting source as a Python expression
        # under a `Vehicle` symbol -> compare to original.
        src = seed_python(original)
        roundtripped = eval(src, {"Vehicle": Vehicle})
        self.assertEqual(roundtripped, original)

    def test_collapses_payload_by_class_to_scalar(self):
        entries = [
            ("obj", "vehicle"),
            ("name", "X"),
            ("waytype", "track"),
            ("payload[0]", "0"),
            ("payload[3]", "18"),
        ]
        v = port_vehicle(entries)
        self.assertEqual(v.payload, 18)
        self.assertEqual(v.payload_by_class, [0, 18])

    def test_harvests_constraints(self):
        entries = [
            ("obj", "vehicle"),
            ("name", "X"),
            ("waytype", "track"),
            ("Constraint[Prev][0]", "any"),
            ("Constraint[Next][0]", "B"),
            ("Constraint[Next][1]", "C"),
        ]
        v = port_vehicle(entries)
        self.assertEqual(v.constraint_prev, ["any"])
        self.assertEqual(v.constraint_next, ["B", "C"])

    def test_rejects_non_vehicle_obj(self):
        with self.assertRaisesRegex(ValueError, "not obj=vehicle"):
            port_vehicle([("obj", "good"), ("name", "X")])


class TestSeedPython(unittest.TestCase):
    def test_omits_default_fields(self):
        src = seed_python(Vehicle(name="A", waytype="track"))
        self.assertIn("name='A'", src)
        self.assertIn("waytype='track'", src)
        self.assertNotIn("copyright", src)
        self.assertNotIn("None", src)

    def test_one_field_per_line(self):
        v = Vehicle(name="A", waytype="track", speed=100, length=3)
        src = seed_python(v)
        # 4 fields -> 4 trailing commas
        self.assertEqual(src.count(","), 4)


if __name__ == "__main__":
    unittest.main()
