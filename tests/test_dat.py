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
    Building,
    Vehicle,
    Way,
    emit_building,
    emit_vehicles,
    emit_way,
    iter_building_cells,
    layouts_default,
    parse,
    port_building,
    port_vehicle,
    port_way,
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


class TestEmitVehicles(unittest.TestCase):
    def _text(self, *vehicles: Vehicle) -> str:
        with TemporaryDirectory() as d:
            return emit_vehicles(list(vehicles), out_dir=Path(d), basename="x").read_text()

    # ---- single-Vehicle structure ----

    def test_minimal_skips_none(self):
        text = self._text(Vehicle(name="A", waytype="track"))
        lines = text.splitlines()
        self.assertEqual(lines[:3], ["obj=vehicle", "name=A", "waytype=track"])
        body = lines[3:lines.index("EmptyImage[S]=./x.0.0")]
        self.assertEqual(body, [])

    def test_emits_extended_fields(self):
        text = self._text(Vehicle(name="A", waytype="track", axles=4,
                                  comfort_by_class=[10, 20]))
        self.assertIn("axles=4\n", text)
        self.assertIn("comfort[0]=10\n", text)
        self.assertIn("comfort[1]=20\n", text)

    def test_scalar_comfort_emits_unindexed(self):
        text = self._text(Vehicle(name="A", waytype="track", comfort=49))
        self.assertIn("comfort=49\n", text)
        self.assertNotIn("comfort[", text)

    def test_payload_by_class_uses_remapped_dat_key(self):
        text = self._text(Vehicle(name="A", waytype="track",
                                  payload_by_class=[0, 0, 0, 18]))
        self.assertIn("payload[3]=18\n", text)
        self.assertNotIn("payload_by_class", text)

    def test_constraint_uses_capitalised_form(self):
        text = self._text(Vehicle(name="A", waytype="track", constraint_next=["B", "C"]))
        self.assertIn("Constraint[Next][0]=B\n", text)
        self.assertIn("Constraint[Next][1]=C\n", text)

    def test_emits_eight_facing_image_refs(self):
        # makeobj parses `<file>.X.Y` as row=X, col=Y, so the single-row
        # hex atlas's 8 facings address as `.0.0` .. `.0.7`.
        text = self._text(Vehicle(name="A", waytype="track"))
        for col, facing in enumerate(("S", "SW", "W", "NW", "N", "NE", "E", "SE")):
            self.assertIn(f"EmptyImage[{facing}]=./x.0.{col}\n", text)

    # ---- multi-Vehicle structure ----

    def test_multi_round_trips_to_n_objects_in_order(self):
        a = Vehicle(name="A", waytype="track", speed=80)
        b = Vehicle(name="B", waytype="track", speed=60)
        with TemporaryDirectory() as d:
            out = emit_vehicles([a, b], out_dir=Path(d), basename="x")
            self.assertEqual([dict(o)["name"] for o in parse(out)], ["A", "B"])

    def test_multi_shares_atlas_refs(self):
        # Shared-sprite variants (dragon-rapide + dragon-rapide-mail) —
        # every block's image refs point at the same atlas.
        text = self._text(Vehicle(name="A", waytype="track"),
                          Vehicle(name="B", waytype="track"))
        self.assertEqual(text.count("EmptyImage[S]=./x.0.0\n"), 2)

    def test_empty_list_rejected(self):
        with TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                emit_vehicles([], out_dir=Path(d), basename="x")


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

    def test_renders_way_constructor(self):
        src = seed_python(Way(name="X", waytype="track"))
        self.assertTrue(src.startswith("Way("))


class TestEmitWay(unittest.TestCase):
    def _emit(self, w: Way) -> str:
        with TemporaryDirectory() as d:
            emit_way(w, out_dir=Path(d), basename="x")
            return (Path(d) / "x.dat").read_text()

    def test_minimal_skips_none(self):
        text = self._emit(Way(name="A", waytype="track"))
        lines = text.splitlines()
        self.assertEqual(lines[0], "obj=way")
        self.assertEqual(lines[1], "name=A")
        self.assertEqual(lines[2], "waytype=track")
        # Body between the scalars and the first image ref carries
        # only the stub cursor/icon refs (option (a) in TODO.md →
        # "Bake hex icon + cursor sprites for ways"); no other
        # `copyright=` / `cost=` etc. lines from unset scalars.
        body = lines[3:lines.index("image[-][0]=./x.0.0")]
        self.assertEqual(body, ["icon=./x.1.6", "cursor=./x.0.0"])

    def test_emits_hex_ribi_atlas_refs(self):
        text = self._emit(Way(name="A", waytype="track"))
        # 64 hex ribi cells: leading "-" + 63 popcount-then-ribi
        # entries, 8 cols x 8 rows.  Pin the boundaries we care
        # about so a future reordering trips the test.
        self.assertIn("image[-][0]=./x.0.0\n", text)
        self.assertIn("image[se][0]=./x.0.1\n", text)
        self.assertIn("image[ne][0]=./x.0.6\n", text)
        self.assertIn("image[se_s][0]=./x.0.7\n", text)
        self.assertIn("image[se_sw][0]=./x.1.0\n", text)
        self.assertIn("image[se_s_sw_nw_n_ne][0]=./x.7.7\n", text)
        # 64 image lines total.
        self.assertEqual(text.count("image["), 64)

    def test_emits_set_scalars_in_field_order(self):
        text = self._emit(Way(name="X", waytype="track", cost=140000,
                              topspeed=160, axle_load=12))
        lines = text.splitlines()
        # Canonical emit order = field order in the dataclass:
        # name, waytype, ..., topspeed, ..., axle_load, ..., cost.
        prefixes = [l.split("=")[0] for l in lines[:6]]
        self.assertEqual(prefixes, ["obj", "name", "waytype",
                                    "topspeed", "axle_load", "cost"])


class TestPortWay(unittest.TestCase):
    def test_round_trips_through_seed_python(self):
        original = Way(
            name="cssr", waytype="track",
            intro_year=1968, intro_month=3,
            topspeed=160, max_weight=22,
            wear_capacity=4128000000,
            cost=140000, maintenance=375,
        )
        src = seed_python(original)
        roundtripped = eval(src, {"Way": Way})
        self.assertEqual(roundtripped, original)

    def test_harvests_engine_scalars(self):
        entries = [
            ("obj", "way"), ("Name", "cssr"), ("waytype", "track"),
            ("cost", "140000"), ("maintenance", "375"),
            ("topspeed", "160"), ("max_weight", "22"),
            ("intro_year", "1968"), ("intro_month", "3"),
            ("wear_capacity", "4128000000"),
        ]
        w = port_way(entries)
        self.assertEqual(w.name, "cssr")
        self.assertEqual(w.cost, 140000)
        self.assertEqual(w.wear_capacity, 4128000000)

    def test_drops_upstream_image_refs(self):
        # Upstream square-ribi image keys are not Way fields and
        # must not surface as kwargs (would TypeError on construction).
        entries = [
            ("obj", "way"), ("Name", "x"), ("waytype", "track"),
            ("Image[NS][0]", "./images/x.1.0"),
            ("ImageUp[3][0]", "./images/x.4.2"),
        ]
        w = port_way(entries)  # must not raise
        self.assertEqual(w.name, "x")

    def test_drops_icon_and_cursor_on_port(self):
        # Upstream `icon=`/`cursor=` reference cells under the pak's
        # stripped images/ dir — they'd make makeobj error out at
        # build time if they survived a port unchanged (see
        # `Way.icon` field doc).  port_way drops them; the bake
        # script's SPEC stays clean.  `emit_way` then fills in stub
        # refs pointing at existing hex-atlas cells so makeobj's
        # cursorskin writer sees a non-empty cursor/icon and the
        # engine's `weg_search` picks the way up as a buildable
        # default (option (a) in TODO.md → "Bake hex icon + cursor
        # sprites for ways").
        entries = [
            ("obj", "way"), ("Name", "x"), ("waytype", "track"),
            ("icon", "> ./images/x.3.4"),
            ("cursor", "./images/x.3.5"),
        ]
        w = port_way(entries)
        self.assertIsNone(w.icon)
        self.assertIsNone(w.cursor)
        with TemporaryDirectory() as d:
            text = emit_way(w, out_dir=Path(d), basename="x").read_text()
        # Stub refs point at hex-atlas cells, not the stripped
        # upstream images/ dir.
        self.assertIn("cursor=./x.0.0", text)
        self.assertIn("icon=./x.1.6", text)
        self.assertNotIn("images/", text)

    def test_rejects_non_way_obj(self):
        with self.assertRaisesRegex(ValueError, "not obj=way"):
            port_way([("obj", "vehicle"), ("name", "X")])


class TestBuildingFootprint(unittest.TestCase):
    def test_layouts_default_square_is_one(self):
        # The engine rule from `building_writer.cc`: square footprints
        # have one layout (no asymmetric rotation), rectangular have two.
        self.assertEqual(layouts_default(1, 1), 1)
        self.assertEqual(layouts_default(2, 2), 1)
        self.assertEqual(layouts_default(3, 3), 1)

    def test_layouts_default_rectangular_is_two(self):
        self.assertEqual(layouts_default(2, 1), 2)
        self.assertEqual(layouts_default(1, 3), 2)
        self.assertEqual(layouts_default(4, 5), 2)

    def test_hex_layouts_default_pins_pak_policy(self):
        # Pak-side bake policy distinct from the engine read-side
        # default — single-tile gets 6 (60° steps, hex-native);
        # rectangular falls back to the engine default until a
        # multi-tile asset pins a different choice.
        from pak.bake import hex_layouts_default
        self.assertEqual(hex_layouts_default(1, 1), 6)
        self.assertEqual(hex_layouts_default(2, 1), 2)
        self.assertEqual(hex_layouts_default(2, 2), 1)

    def test_resolve_building_layouts_fills_in_none(self):
        from pak.bake import _resolve_building_layouts
        # None → hex default; an explicit value passes through.
        none = Building(name="X", type="res", dims_x=1, dims_y=1)
        self.assertEqual(_resolve_building_layouts(none).layouts, 6)
        pinned = Building(name="X", type="res", dims_x=1, dims_y=1, layouts=4)
        self.assertEqual(_resolve_building_layouts(pinned).layouts, 4)

    def test_iter_cells_square_footprint(self):
        # 2x2 with default layouts=1, heights=1: 4 cells, (y, x) row-major.
        b = Building(name="X", type="mon", dims_x=2, dims_y=2)
        cells = list(iter_building_cells(b))
        self.assertEqual(cells, [
            (0, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 0), (0, 1, 1, 0),
        ])

    def test_iter_cells_rectangular_swaps_on_odd_layouts(self):
        # 2x1 with default layouts=2: layout 0 has h=size.y=1 w=size.x=2;
        # layout 1 has h=size.x=2 w=size.y=1 (engine's `h = (l&1) ?
        # size.x : size.y`).  Pin both bounds explicitly.
        b = Building(name="X", type="cur", dims_x=2, dims_y=1)
        cells = list(iter_building_cells(b))
        self.assertEqual(cells, [
            (0, 0, 0, 0), (0, 0, 1, 0),  # layout 0: y in [0,1), x in [0,2)
            (1, 0, 0, 0), (1, 1, 0, 0),  # layout 1: y in [0,2), x in [0,1)
        ])

    def test_iter_cells_explicit_four_layouts(self):
        # 1x1x4: square footprint but explicit layouts=4 — common upstream
        # pattern (the four map rotations of a non-rotationally-symmetric
        # asset packed into one tile).
        b = Building(name="X", type="cur", dims_x=1, dims_y=1, layouts=4)
        cells = list(iter_building_cells(b))
        self.assertEqual(cells, [(l, 0, 0, 0) for l in range(4)])

    def test_iter_cells_height_stack(self):
        # 1x1x1 with heights=2: each (l,y,x) yields 2 heights (h=0, h=1).
        b = Building(name="X", type="res", dims_x=1, dims_y=1, heights=2)
        cells = list(iter_building_cells(b))
        # Single layout (square default), single tile, two heights.
        self.assertEqual(cells, [(0, 0, 0, 0), (0, 0, 0, 1)])

    def test_iter_cells_layouts_x_heights(self):
        # Layouts and heights compose: 4 layouts × 2 heights = 8 cells,
        # height inner (height varies fastest after layout fixes l/y/x).
        b = Building(name="X", type="res",
                     dims_x=1, dims_y=1, layouts=4, heights=2)
        cells = list(iter_building_cells(b))
        self.assertEqual(cells, [
            (0, 0, 0, 0), (0, 0, 0, 1),
            (1, 0, 0, 0), (1, 0, 0, 1),
            (2, 0, 0, 0), (2, 0, 0, 1),
            (3, 0, 0, 0), (3, 0, 0, 1),
        ])


class TestEmitBuilding(unittest.TestCase):
    def _emit(self, b: Building) -> str:
        with TemporaryDirectory() as d:
            emit_building(b, out_dir=Path(d), basename="x")
            return (Path(d) / "x.dat").read_text()

    def test_minimal_skips_none(self):
        text = self._emit(Building(name="A", type="mon"))
        lines = text.splitlines()
        self.assertEqual(lines[0], "obj=building")
        self.assertEqual(lines[1], "name=A")
        self.assertEqual(lines[2], "type=mon")
        # Default 1x1 footprint → one cell, dims emitted with engine-
        # default layouts=1.
        self.assertIn("dims=1,1,1", lines)
        self.assertIn("backimage[0][0][0][0][0][0]=./x.0.0", lines)

    def test_emits_dims_with_explicit_layouts(self):
        b = Building(name="A", type="mon", dims_x=2, dims_y=2, layouts=1)
        text = self._emit(b)
        self.assertIn("dims=2,2,1\n", text)

    def test_rectangular_default_layouts_filled_in(self):
        # SPEC leaves layouts=None; emit fills 2 (rectangular default).
        b = Building(name="A", type="mon", dims_x=2, dims_y=1)
        text = self._emit(b)
        self.assertIn("dims=2,1,2\n", text)

    def test_emits_square_2x2_cells_one_layout(self):
        # nelson-column shape: dims=2,2,1 → one layout × four cells.
        b = Building(name="A", type="mon", dims_x=2, dims_y=2)
        text = self._emit(b)
        self.assertIn("backimage[0][0][0][0][0][0]=./x.0.0\n", text)
        self.assertIn("backimage[0][0][1][0][0][0]=./x.0.1\n", text)
        self.assertIn("backimage[0][1][0][0][0][0]=./x.0.2\n", text)
        self.assertIn("backimage[0][1][1][0][0][0]=./x.0.3\n", text)
        # No other layouts.
        self.assertNotIn("backimage[1]", text)

    def test_emits_four_layouts_for_1x1_rotation_variant(self):
        # 1x1x4 — four rotations of a single tile.  One cell per
        # layout, atlased as `.<layout>.0`.
        b = Building(name="A", type="cur", dims_x=1, dims_y=1, layouts=4)
        text = self._emit(b)
        for l in range(4):
            self.assertIn(
                f"backimage[{l}][0][0][0][0][0]=./x.{l}.0\n", text)

    def test_emits_rectangular_swaps_y_x_on_odd_layouts(self):
        # 2x1x2: layout 0 cells (y=0,x=0) (y=0,x=1); layout 1 (swap)
        # cells (y=0,x=0) (y=1,x=0).
        b = Building(name="A", type="cur", dims_x=2, dims_y=1)
        text = self._emit(b)
        self.assertIn("backimage[0][0][0][0][0][0]=./x.0.0\n", text)
        self.assertIn("backimage[0][0][1][0][0][0]=./x.0.1\n", text)
        self.assertIn("backimage[1][0][0][0][0][0]=./x.1.0\n", text)
        self.assertIn("backimage[1][1][0][0][0][0]=./x.1.1\n", text)

    def test_emits_height_stack_row_index(self):
        # heights=2 — atlas row = layout * heights + height.
        # 1x1, layouts=2, heights=2: rows 0..3 = (l,h) = (0,0),(0,1),(1,0),(1,1).
        b = Building(name="A", type="res",
                     dims_x=1, dims_y=1, layouts=2, heights=2)
        text = self._emit(b)
        self.assertIn("backimage[0][0][0][0][0][0]=./x.0.0\n", text)  # l=0 h=0 -> row 0
        self.assertIn("backimage[0][0][0][1][0][0]=./x.1.0\n", text)  # l=0 h=1 -> row 1
        self.assertIn("backimage[1][0][0][0][0][0]=./x.2.0\n", text)  # l=1 h=0 -> row 2
        self.assertIn("backimage[1][0][0][1][0][0]=./x.3.0\n", text)  # l=1 h=1 -> row 3

    def test_emits_set_scalars_in_field_order(self):
        b = Building(name="A", type="mon", copyright="Kieron",
                     intro_year=1850, level=20, chance=10)
        text = self._emit(b)
        lines = text.splitlines()
        prefixes = [l.split("=")[0] for l in lines[:7]]
        # Canonical order = field order in the dataclass.
        self.assertEqual(prefixes, [
            "obj", "name", "type", "copyright", "level", "chance",
            "intro_year",
        ])

    def test_emits_class_proportion_indexed(self):
        b = Building(name="A", type="cur",
                     class_proportion=[10, 10, 25, 25, 30])
        text = self._emit(b)
        for i, v in enumerate([10, 10, 25, 25, 30]):
            self.assertIn(f"class_proportion[{i}]={v}\n", text)


class TestPortBuilding(unittest.TestCase):
    def test_round_trips_through_seed_python(self):
        original = Building(
            name="NelsonColumn2", type="mon",
            copyright="James", level=20, chance=10,
            intro_year=1806, intro_month=1,
            retire_year=1880, retire_month=1,
            needs_ground=1,
            dims_x=2, dims_y=2, layouts=1,
            class_proportion=[10, 10, 25, 25, 30],
        )
        src = seed_python(original)
        roundtripped = eval(src, {"Building": Building})
        self.assertEqual(roundtripped, original)

    def test_harvests_dims_and_scalars(self):
        # Mirrors nelson-column.dat shape (with both `Dims=` and the
        # extended `population_and_visitor_demand_capacity` key).
        entries = [
            ("obj", "building"),
            ("name", "NelsonColumn2"),
            ("type", "mon"),
            ("Dims", "2,2,1"),
            ("level", "20"),
            ("chance", "10"),
            ("population_and_visitor_demand_capacity", "32"),
            ("class_proportion[0]", "10"),
            ("class_proportion[1]", "10"),
            ("class_proportion[2]", "25"),
            ("class_proportion[3]", "25"),
            ("class_proportion[4]", "30"),
        ]
        b = port_building(entries)
        self.assertEqual(b.name, "NelsonColumn2")
        self.assertEqual(b.type, "mon")
        self.assertEqual((b.dims_x, b.dims_y, b.layouts), (2, 2, 1))
        self.assertEqual(b.level, 20)
        self.assertEqual(b.population_and_visitor_demand_capacity, 32)
        self.assertEqual(b.class_proportion, [10, 10, 25, 25, 30])

    def test_harvests_two_value_dims(self):
        # `Dims=X,Y` without explicit layouts — the seeder records
        # layouts=None so emit_building can fall back to the engine
        # default at write time.
        entries = [
            ("obj", "building"), ("name", "X"), ("type", "cur"),
            ("dims", "2,5"),
        ]
        b = port_building(entries)
        self.assertEqual((b.dims_x, b.dims_y, b.layouts), (2, 5, None))

    def test_drops_upstream_image_refs(self):
        # Upstream `BackImage[…]=images/<type>/<name>.X.Y` refs target
        # the stripped images/ dir — the hex bake re-emits them from
        # its own atlas.  port_building drops them so seeded SPECs
        # bake cleanly without scrubbing.
        entries = [
            ("obj", "building"), ("name", "X"), ("type", "cur"),
            ("Dims", "1,1,4"),
            ("BackImage[0][0][0][0][0][0]", "images/cur/x.0.0"),
            ("BackImage[1][0][0][0][0][0]", "images/cur/x.0.1"),
            ("FrontImage[0][0][0][0][0][0]", "images/cur/x.1.0"),
        ]
        b = port_building(entries)  # must not raise
        self.assertEqual(b.name, "X")
        self.assertEqual((b.dims_x, b.dims_y, b.layouts), (1, 1, 4))

    def test_harvests_heights_from_backimage_keys(self):
        # Building has stacked height levels; port_building reads the
        # max height index seen and sets `heights = max + 1`.
        entries = [
            ("obj", "building"), ("name", "X"), ("type", "res"),
            ("dims", "1,1,1"),
            ("BackImage[0][0][0][0][0][0]", "images/res/x.0.0"),
            ("BackImage[0][0][0][1][0][0]", "images/res/x.1.0"),
            ("BackImage[0][0][0][2][0][0]", "images/res/x.2.0"),
        ]
        b = port_building(entries)
        self.assertEqual(b.heights, 3)

    def test_rejects_non_building_obj(self):
        with self.assertRaisesRegex(ValueError, "not obj=building"):
            port_building([("obj", "way"), ("name", "X"), ("type", "mon")])

    def test_seed_python_renders_building_constructor(self):
        src = seed_python(Building(name="X", type="cur"))
        self.assertTrue(src.startswith("Building("))


if __name__ == "__main__":
    unittest.main()
