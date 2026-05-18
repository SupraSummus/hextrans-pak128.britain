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
    HEX_BRIDGE_PIECE_LABELS,
    HEX_BRIDGE_PIECE_ORDER,
    TREE_AGE_COUNT,
    Bridge,
    Building,
    Tree,
    Vehicle,
    Way,
    building_footprint_centroid,
    emit_bridge,
    emit_building,
    emit_trees,
    emit_vehicles,
    emit_way,
    iter_building_cells,
    layouts_default,
    parse,
    port_bridge,
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

    def test_strips_trailing_inline_comment(self):
        # Upstream ships values followed by ` # ...` comments
        # (way_constraint_prohibitive[6]=6 # Large ship); without
        # stripping, port_vehicle's _coerce keeps the comment in
        # the value as a string.
        with TemporaryDirectory() as d:
            p = Path(d) / "x.dat"
            p.write_text("obj=vehicle\nspeed=12 # knots\nname=x\t# tab\n")
            (obj,) = parse(p)
        self.assertEqual(dict(obj), {"obj": "vehicle", "speed": "12", "name": "x"})


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


class TestEmitBridge(unittest.TestCase):
    def _emit(self, b: Bridge) -> str:
        with TemporaryDirectory() as d:
            emit_bridge(b, out_dir=Path(d), basename="x")
            return (Path(d) / "x.dat").read_text()

    def test_minimal_skips_none(self):
        text = self._emit(Bridge(name="A", waytype="track"))
        lines = text.splitlines()
        self.assertEqual(lines[0], "obj=bridge")
        self.assertEqual(lines[1], "name=A")
        self.assertEqual(lines[2], "waytype=track")
        # Unset scalars are skipped; the only body lines before the
        # first image ref are the stub icon/cursor (emit_bridge fills
        # them in when the SPEC left them None).
        body = lines[3:lines.index("BackImage[n_s][0]=./x.0.0")]
        self.assertEqual(body, ["icon=./x.0.0", "cursor=./x.1.0"])

    def test_emits_back_and_front_for_each_label(self):
        text = self._emit(Bridge(name="A", waytype="track"))
        for row, piece in enumerate(HEX_BRIDGE_PIECE_ORDER):
            key = piece.capitalize()  # image -> Image, start -> Start, ramp -> Ramp
            for col, label in enumerate(HEX_BRIDGE_PIECE_LABELS[piece]):
                cell = f"./x.{row}.{col}"
                self.assertIn(f"Back{key}[{label}][0]={cell}\n", text)
                self.assertIn(f"Front{key}[{label}][0]={cell}\n", text)
        # Sanity on the totals: every label has both a Back and Front
        # line, no extras.
        total_labels = sum(len(v) for v in HEX_BRIDGE_PIECE_LABELS.values())
        self.assertEqual(text.count("[0]=./x."), 2 * total_labels)

    def test_emits_set_scalars_in_field_order(self):
        text = self._emit(Bridge(
            name="X", waytype="track",
            intro_year=1890, topspeed=160,
            cost=2760000, pillar_distance=2,
        ))
        prefixes = [l.split("=")[0] for l in text.splitlines()[:6]]
        # Field order in the dataclass: name, waytype, ..., intro_year,
        # ..., topspeed, ..., cost, ..., pillar_distance.
        self.assertEqual(prefixes, ["obj", "name", "waytype",
                                    "intro_year", "topspeed", "cost"])

    def test_icon_and_cursor_overrides_keep_spec_value(self):
        text = self._emit(Bridge(name="A", waytype="track",
                                 icon="./custom.9.9", cursor="./other.8.8"))
        self.assertIn("icon=./custom.9.9", text)
        self.assertIn("cursor=./other.8.8", text)


class TestPortBridge(unittest.TestCase):
    def test_round_trips_through_seed_python(self):
        original = Bridge(
            name="PlateGirder", waytype="track", copyright="kieron/James",
            intro_year=1890, intro_month=9,
            retire_year=1949, retire_month=1,
            topspeed=160, max_weight=400, max_length=4,
            cost=2760000, maintenance=100,
            has_own_way_graphics=0,
            pillar_distance=2, pillar_asymmetric=1,
        )
        src = seed_python(original)
        roundtripped = eval(src, {"Bridge": Bridge})
        self.assertEqual(roundtripped, original)

    def test_drops_upstream_image_refs(self):
        # Upstream Back/FrontImage / Start / Ramp and the variant-2
        # cousins (BackImage2 etc.) must not surface as kwargs
        # (would TypeError on construction).
        entries = [
            ("obj", "bridge"), ("name", "X"), ("waytype", "track"),
            ("BackImage[NS][0]",  "./images/x.0.5,0,32"),
            ("FrontStart[E][1]",  "./images/x-snow.1.1,0,32"),
            ("BackRamp[N][0]",    "./images/x.0.6"),
            ("BackImage2[EW][0]", "./images/x.2.4,0,32"),
            ("backPillar[S][0]",  "./images/x.4.3"),
        ]
        b = port_bridge(entries)
        self.assertEqual(b.name, "X")

    def test_drops_icon_and_cursor_on_port(self):
        # Same convention as port_way: upstream icon/cursor cells live
        # under the stripped images/ dir; emit_bridge fills in stub
        # refs pointing at existing atlas cells.
        entries = [
            ("obj", "bridge"), ("name", "X"), ("waytype", "track"),
            ("icon", "> ./images/x.4.0"),
            ("cursor", "./images/x.4.1"),
        ]
        b = port_bridge(entries)
        self.assertIsNone(b.icon)
        self.assertIsNone(b.cursor)
        with TemporaryDirectory() as d:
            text = emit_bridge(b, out_dir=Path(d), basename="x").read_text()
        self.assertIn("icon=./x.0.0", text)
        self.assertIn("cursor=./x.1.0", text)
        self.assertNotIn("images/", text)

    def test_harvests_engine_scalars(self):
        # Lift directly from the upstream plate-girder.dat shape -- the
        # exact field set port_bridge needs to harvest for a paste-
        # ready SPEC.  Casing varies in upstream dats; lookup is case-
        # insensitive.
        entries = [
            ("obj", "bridge"), ("Name", "PlateGirder"),
            ("waytype", "track"), ("copyright", "kieron/James"),
            ("intro_year", "1890"), ("retire_year", "1949"),
            ("topspeed", "160"), ("max_weight", "400"),
            ("cost", "2760000"), ("maintenance", "100"),
            ("pillar_distance", "2"), ("pillar_asymmetric", "1"),
            ("has_own_way_graphics", "0"),
        ]
        b = port_bridge(entries)
        self.assertEqual(b.name, "PlateGirder")
        self.assertEqual(b.topspeed, 160)
        self.assertEqual(b.cost, 2760000)
        self.assertEqual(b.pillar_asymmetric, 1)

    def test_rejects_non_bridge_obj(self):
        with self.assertRaisesRegex(ValueError, "not obj=bridge"):
            port_bridge([("obj", "way"), ("name", "X")])


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
        # 2x2 with default layouts=1, heights=1, seasons=1: 4 cells,
        # (y, x) row-major.  Tuple shape is (s, l, y, x, h).
        b = Building(name="X", type="mon", dims_x=2, dims_y=2)
        cells = list(iter_building_cells(b))
        self.assertEqual(cells, [
            (0, 0, 0, 0, 0), (0, 0, 0, 1, 0),
            (0, 0, 1, 0, 0), (0, 0, 1, 1, 0),
        ])

    def test_iter_cells_rectangular_swaps_on_odd_layouts(self):
        # 2x1 with default layouts=2: layout 0 has h=size.y=1 w=size.x=2;
        # layout 1 has h=size.x=2 w=size.y=1 (engine's `h = (l&1) ?
        # size.x : size.y`).  Pin both bounds explicitly.
        b = Building(name="X", type="cur", dims_x=2, dims_y=1)
        cells = list(iter_building_cells(b))
        self.assertEqual(cells, [
            (0, 0, 0, 0, 0), (0, 0, 0, 1, 0),  # l=0: y in [0,1), x in [0,2)
            (0, 1, 0, 0, 0), (0, 1, 1, 0, 0),  # l=1: y in [0,2), x in [0,1)
        ])

    def test_iter_cells_explicit_four_layouts(self):
        # 1x1x4: square footprint but explicit layouts=4 — common upstream
        # pattern (the four map rotations of a non-rotationally-symmetric
        # asset packed into one tile).
        b = Building(name="X", type="cur", dims_x=1, dims_y=1, layouts=4)
        cells = list(iter_building_cells(b))
        self.assertEqual(cells, [(0, l, 0, 0, 0) for l in range(4)])

    def test_iter_cells_height_stack(self):
        # 1x1x1 with heights=2: each height yields one cell.  Height is
        # outer to layout, so consecutive cells are (h=0, then h=1).
        b = Building(name="X", type="res", dims_x=1, dims_y=1, heights=2)
        cells = list(iter_building_cells(b))
        self.assertEqual(cells, [(0, 0, 0, 0, 0), (0, 0, 0, 0, 1)])

    def test_iter_cells_layouts_x_heights(self):
        # Layouts and heights compose: 4 layouts × 2 heights = 8 cells.
        # Height is outer to layout — each (s, h) is one atlas row,
        # layouts span columns within the row.  Order: (h=0, l=0..3),
        # (h=1, l=0..3).
        b = Building(name="X", type="res",
                     dims_x=1, dims_y=1, layouts=4, heights=2)
        cells = list(iter_building_cells(b))
        self.assertEqual(cells, [
            (0, 0, 0, 0, 0), (0, 1, 0, 0, 0),  # h=0: l=0..3
            (0, 2, 0, 0, 0), (0, 3, 0, 0, 0),
            (0, 0, 0, 0, 1), (0, 1, 0, 0, 1),  # h=1: l=0..3
            (0, 2, 0, 0, 1), (0, 3, 0, 0, 1),
        ])

    def test_iter_cells_seasons_outermost(self):
        # seasons=2 doubles cells; season is outermost so summer block
        # comes first, then winter block.  1x1x2 layouts: 2 cells per
        # season → 4 total.
        b = Building(name="X", type="res", dims_x=1, dims_y=1,
                     layouts=2, seasons=2)
        cells = list(iter_building_cells(b))
        self.assertEqual(cells, [
            (0, 0, 0, 0, 0), (0, 1, 0, 0, 0),  # summer: l=0, l=1
            (1, 0, 0, 0, 0), (1, 1, 0, 0, 0),  # winter: l=0, l=1
        ])


class TestBuildingFootprintCentroid(unittest.TestCase):
    def test_square_footprint_constant_across_layouts(self):
        # 2x2: even/odd dim swap is a no-op, centroid is (0.5, 0.5) for
        # every L.  Pins the "no-op when dims are square" property.
        for l in range(4):
            self.assertEqual(
                building_footprint_centroid(2, 2, l), (0.5, 0.5),
            )

    def test_rectangular_footprint_swaps_on_odd_layouts(self):
        # 2x1: even L has cells (y=0, x=0..1) -> centroid (0.5, 0);
        # odd L has cells (y=0..1, x=0) -> centroid (0, 0.5).  Mirrors
        # the engine's per-L `(y, x)` cell-range swap.
        self.assertEqual(building_footprint_centroid(2, 1, 0), (0.5, 0.0))
        self.assertEqual(building_footprint_centroid(2, 1, 1), (0.0, 0.5))
        self.assertEqual(building_footprint_centroid(2, 1, 2), (0.5, 0.0))
        self.assertEqual(building_footprint_centroid(2, 1, 3), (0.0, 0.5))

    def test_single_tile_is_zero(self):
        self.assertEqual(building_footprint_centroid(1, 1, 0), (0.0, 0.0))


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
        # 1x1x4 — four rotations of a single tile.  One row × four
        # columns: layouts span the columns left-to-right.
        b = Building(name="A", type="cur", dims_x=1, dims_y=1, layouts=4)
        text = self._emit(b)
        for l in range(4):
            self.assertIn(
                f"backimage[{l}][0][0][0][0][0]=./x.0.{l}\n", text)

    def test_emits_rectangular_swaps_y_x_on_odd_layouts(self):
        # 2x1x2: layout 0 cells at cols 0..1, layout 1 cells at cols 2..3.
        # `col = l * dims_x*dims_y + y*w + x`.
        b = Building(name="A", type="cur", dims_x=2, dims_y=1)
        text = self._emit(b)
        self.assertIn("backimage[0][0][0][0][0][0]=./x.0.0\n", text)
        self.assertIn("backimage[0][0][1][0][0][0]=./x.0.1\n", text)
        self.assertIn("backimage[1][0][0][0][0][0]=./x.0.2\n", text)
        self.assertIn("backimage[1][1][0][0][0][0]=./x.0.3\n", text)

    def test_emits_height_stack_row_index(self):
        # heights=2 — each height is its own atlas row, layouts span
        # columns.  1x1, layouts=2, heights=2 → 2 rows × 2 cols.
        # Row = s*heights + h = h; col = l.
        b = Building(name="A", type="res",
                     dims_x=1, dims_y=1, layouts=2, heights=2)
        text = self._emit(b)
        self.assertIn("backimage[0][0][0][0][0][0]=./x.0.0\n", text)  # h=0 l=0
        self.assertIn("backimage[1][0][0][0][0][0]=./x.0.1\n", text)  # h=0 l=1
        self.assertIn("backimage[0][0][0][1][0][0]=./x.1.0\n", text)  # h=1 l=0
        self.assertIn("backimage[1][0][0][1][0][0]=./x.1.1\n", text)  # h=1 l=1

    def test_emits_seasons_top_summer_bottom_winter(self):
        # 1x1x4 layouts, seasons=2 → 2 rows × 4 cols.  Summer cells
        # (season=0) land on row 0; winter cells (season=1) land on
        # row 1.  Matches upstream `1600-detatched-house-2f.png`.
        b = Building(name="A", type="res",
                     dims_x=1, dims_y=1, layouts=4, seasons=2)
        text = self._emit(b)
        for l in range(4):
            self.assertIn(
                f"backimage[{l}][0][0][0][0][0]=./x.0.{l}\n", text)  # summer
            self.assertIn(
                f"backimage[{l}][0][0][0][0][1]=./x.1.{l}\n", text)  # winter

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


class TestEmitTrees(unittest.TestCase):
    def _text(self, *trees: Tree, **kw) -> str:
        with TemporaryDirectory() as d:
            return emit_trees(list(trees), out_dir=Path(d), basename="oak",
                              **kw).read_text()

    def test_emits_five_age_keys_per_season(self):
        # Engine reads exactly 5 ages.  With seasons=1 that's 5 keys;
        # with seasons=5 that's 25.  No upstream caller can negotiate
        # this -- the writer hardcodes the loop bound.
        for seasons in (1, 2, 5):
            text = self._text(Tree(name="X", seasons=seasons))
            for a in range(TREE_AGE_COUNT):
                for s in range(seasons):
                    self.assertIn(f"image[{a}][{s}]=./oak.{s}.{a}\n", text)

    def test_age_overrides_redirect_specific_cells(self):
        # Upstream's "age 4 → winter-3" convention plus our generic
        # clamp both compose into one `age_overrides` table.
        text = self._text(
            Tree(name="X", seasons=5),
            age_overrides={(4, 0): (3, 2)},
        )
        self.assertIn("image[4][0]=./oak.2.3\n", text)
        # Untouched cells emit their natural mapping.
        self.assertIn("image[3][0]=./oak.0.3\n", text)

    def test_seasons_scalar_emits_explicitly(self):
        # `seasons` is the one Tree scalar the engine reads as a
        # required key even though it has a default; we always emit it.
        text = self._text(Tree(name="X", seasons=1))
        self.assertIn("seasons=1\n", text)

    def test_multi_tree_round_trips(self):
        # Multi-Tree atlas-sharing (upstream's `tree.dat` packs four
        # species in one file).
        a = Tree(name="A", seasons=1)
        b = Tree(name="B", seasons=2, climates="tundra")
        with TemporaryDirectory() as d:
            out = emit_trees([a, b], out_dir=Path(d), basename="oak")
            self.assertEqual([dict(o)["name"] for o in parse(out)], ["A", "B"])

    def test_empty_list_rejected(self):
        with self.assertRaises(ValueError):
            emit_trees([], out_dir=Path("/tmp"), basename="oak")


class TestClampAgeOverrides(unittest.TestCase):
    """Engine reads `TREE_AGE_COUNT` (= 5) ages; bakes typically render
    fewer.  `clamp_age_overrides` builds the fallback dict mapping
    every unrendered age slot to the last rendered one of the same
    season -- bake-side and reemit-side both use it so the committed
    dat round-trips."""

    def test_clamps_above_rendered_ages(self):
        from pak.bake import clamp_age_overrides
        overrides = clamp_age_overrides(seasons=1, ages=4)
        self.assertEqual(overrides, {(4, 0): (3, 0)})

    def test_clamps_every_season(self):
        from pak.bake import clamp_age_overrides
        overrides = clamp_age_overrides(seasons=2, ages=3)
        self.assertEqual(overrides, {
            (3, 0): (2, 0), (3, 1): (2, 1),
            (4, 0): (2, 0), (4, 1): (2, 1),
        })

    def test_empty_when_all_ages_rendered(self):
        from pak.bake import clamp_age_overrides
        self.assertEqual(
            clamp_age_overrides(seasons=5, ages=TREE_AGE_COUNT),
            {},
        )


if __name__ == "__main__":
    unittest.main()
