"""Tests for `pak.viewpoints` -- the per-camera + per-viewpoint helpers
shared by hex and square render paths.

Run from the repo root:

    python3 -m unittest tests.test_viewpoints
"""

from __future__ import annotations

import math
import unittest

from pak.dat import building_footprint_centroid
from pak.materials import Lighting
from pak.render import CYCLES, EEVEE, BlendAuthored
from pak.viewpoints import (
    DEFAULT_W,
    HEX_VIEWPOINT,
    SQUARE_VIEWPOINT,
    bridge_hex_viewpoint,
    bridge_square_viewpoint,
    building_hex_viewpoint,
    building_square_viewpoint,
    fence_square_viewpoint,
    hex_tile_pixel_mask,
    hex_tile_screen_offset,
    sq_tile_pixel_mask,
    sun_rotation_for_camera,
    tree_hex_viewpoint,
    tree_square_viewpoint,
    tunnel_hex_viewpoint,
    tunnel_square_viewpoint,
)


class TestSunRotationForCamera(unittest.TestCase):
    """The screen-relative sun-rotation helper.  Single source of truth
    used by both square (cam_z varies per facing) and hex (cam_z=0)
    building viewpoints; calibration drift here lands the building
    sun in the wrong place across both."""

    def test_default_zero_cam(self):
        # cam_z=0 + default az_offset=-90 + default elev=30:
        #   sun_x = 90 - 30 = 60 deg, sun_z = 0 + (-90) = -90 deg
        # Calibrated EEVEE-substitution direction; literal upstream
        # values (elev=0, az=+45) give visibly worse dRGB under EEVEE.
        rx, ry, rz = sun_rotation_for_camera(0.0)
        self.assertAlmostEqual(math.degrees(rx), 60.0)
        self.assertAlmostEqual(ry, 0.0)
        self.assertAlmostEqual(math.degrees(rz), -90.0)

    def test_az_offset_tracks_camera(self):
        # Rotating cam_z by N should rotate sun_z by exactly N.
        for cam_z in (0, 45, 90, 135, 225, 315, -30):
            _, _, rz = sun_rotation_for_camera(float(cam_z))
            self.assertAlmostEqual(
                math.degrees(rz), cam_z - 90.0,
                msg=f"cam_z={cam_z} az broke",
            )

    def test_elevation_maps_to_rotation_x(self):
        # sun_x = 90 - elev: rotation_x=0 means straight-down (Blender
        # SUN emits in local -Z); 90 means horizontal.
        for elev_deg in (0, 30, 45, 60, 90):
            rx, _, _ = sun_rotation_for_camera(0.0, sun_elev_deg=elev_deg)
            self.assertAlmostEqual(math.degrees(rx), 90.0 - elev_deg)


class TestBuildingViewpoints(unittest.TestCase):
    """Square and hex building viewpoints both source their sun rotation
    from `sun_rotation_for_camera`.  Spot-check that a change in the
    helper's defaults would flow into both viewpoints in lockstep
    (the whole point of factoring it out)."""

    def test_square_facings_have_per_camera_sun(self):
        vp = building_square_viewpoint(layouts=4, units_per_tile=12.0)
        self.assertEqual(len(vp.facings), 4)
        # Each cardinal camera should have a different sun rotation_z,
        # offset by -90 degrees from its cam rotation_z.
        for f in vp.facings:
            cam_z = f.camera_rotation_euler[2]
            sun_z = f.sun_rotation_euler[2]
            self.assertAlmostEqual(sun_z - cam_z, math.radians(-90.0),
                                   places=6)

    def test_hex_building_facings_share_one_sun_rot(self):
        # Hex camera doesn't rotate; sun rotation must be identical for
        # every cell, equal to `sun_rotation_for_camera(0)`.
        vp = building_hex_viewpoint(layouts=6, units_per_tile=12.0, dims_x=1, dims_y=1)
        expected = sun_rotation_for_camera(0.0)
        for f in vp.facings:
            for got, want in zip(f.sun_rotation_euler, expected, strict=True):
                self.assertAlmostEqual(got, want, places=6)

    def test_engine_per_viewpoint(self):
        # Calibration target lock: vehicles + ways need CYCLES (upstream
        # was Cycles); buildings need EEVEE (BI texture rebinding +
        # Lambert shading land closer to upstream's BI output there).
        self.assertIs(SQUARE_VIEWPOINT.engine, CYCLES)
        self.assertIs(HEX_VIEWPOINT.engine, CYCLES)
        self.assertIs(building_square_viewpoint(layouts=4, units_per_tile=12.0).engine, EEVEE)
        self.assertIs(building_hex_viewpoint(layouts=6, units_per_tile=12.0, dims_x=1, dims_y=1).engine,
                      EEVEE)


class TestBuildingHexNTile(unittest.TestCase):
    """`building_hex_viewpoint`: one Facing per (layout, height) with
    `dims_x * dims_y` slices at hex koord screen positions.  Catches
    structural drift in the slice-list generation that would silently
    scramble the atlas's per-cell labels."""

    def test_single_tile_collapses_to_one_slice_at_origin(self):
        # 1×1 is the degenerate N-tile case: one slice per facing at
        # offset (0, 0), canvas collapses to sprite size.
        vp = building_hex_viewpoint(layouts=6, units_per_tile=12.0, dims_x=1, dims_y=1)
        self.assertEqual(len(vp.facings), 6)
        self.assertEqual(vp.canvas_width, DEFAULT_W)
        self.assertEqual(vp.canvas_height, DEFAULT_W)
        for f in vp.facings:
            self.assertEqual(len(f.slices), 1)
            self.assertEqual(f.slices[0].offset, (0, 0))
            self.assertIsNone(f.slices[0].alpha_mask)

    def test_multi_tile_emits_one_facing_per_layout_with_slices(self):
        # 2x1x4 (mechanical-signalbox-large shape): 4 layouts × 1 height
        # = 4 facings; each carries 2 slices (the per-layout cell count
        # under iter_building_cells, regardless of even/odd swap).
        vp = building_hex_viewpoint(layouts=4, units_per_tile=12.0, dims_x=2, dims_y=1)
        self.assertEqual(len(vp.facings), 4)
        for f in vp.facings:
            self.assertIsNotNone(f.slices)
            self.assertEqual(len(f.slices), 2)
        self.assertGreater(vp.canvas_width, DEFAULT_W)

    def test_fit_matrix_anchored_on_units_per_tile(self):
        # `units_per_tile * max_dims` blend units (the per-layout world
        # width the camera covers) map to `max_dims` engine tiles
        # (= 2R*max_dims engine world units); fit scale = `2R /
        # (units_per_tile * max_dims)`.  Independent of the blend's
        # authored ortho_scale.
        from pak.viewpoints import HEX_TILE_RADIUS
        single = building_hex_viewpoint(layouts=6, units_per_tile=12.0, dims_x=1, dims_y=1)
        multi = building_hex_viewpoint(layouts=4, units_per_tile=12.0, dims_x=2, dims_y=1)
        big = BlendAuthored(ortho_scale=999.0)
        self.assertAlmostEqual(single.fit_matrix(big)[0][0],
                               2.0 * HEX_TILE_RADIUS / 12.0, places=6)
        self.assertAlmostEqual(multi.fit_matrix(big)[0][0],
                               2.0 * HEX_TILE_RADIUS / 24.0, places=6)

    def test_fit_matrix_ignores_authored_ortho(self):
        # SPEC's units_per_tile is canonical; the blend's authored
        # ortho_scale shouldn't influence rendering.
        vp = building_hex_viewpoint(
            layouts=4, units_per_tile=24.0, dims_x=2, dims_y=2,
        )
        m12 = vp.fit_matrix(BlendAuthored(ortho_scale=12.0))[0][0]
        m72 = vp.fit_matrix(BlendAuthored(ortho_scale=72.0))[0][0]
        self.assertAlmostEqual(m12, m72, places=9)

    def test_multi_tile_slice_labels_follow_iter_order(self):
        # Atlas col formula `l * dims_x*dims_y + y * w + x` is the
        # contract that lines slices up against `emit_building`'s
        # BackImage references.  Even L=0 (dims_y=1 outer, dims_x=2
        # inner) and odd L=1 (dims_x=2 outer, dims_y=1 inner -- swap)
        # must hit the same (Y, X) label pairs in iter order.
        vp = building_hex_viewpoint(layouts=4, units_per_tile=12.0, dims_x=2, dims_y=1)
        labels_per_layout = {f.label: [s[0] for s in f.slices]
                             for f in vp.facings}
        self.assertEqual(labels_per_layout["L0_H0"],
                         ["L0_Y0_X0_H0", "L0_Y0_X1_H0"])
        # L=1 swap: y iterates over dims_x=2, x over dims_y=1.
        self.assertEqual(labels_per_layout["L1_H0"],
                         ["L1_Y0_X0_H0", "L1_Y1_X0_H0"])

    def test_multi_tile_slice_centres_match_hex_screen_lattice(self):
        # The slice offsets must reproduce the engine's per-tile screen
        # positions relative to the per-layout footprint centroid: the
        # model renders at world origin (canvas centre), so each slice
        # window sits at `hex_tile_screen_offset(x, y) -
        # hex_tile_screen_offset(centroid_x, centroid_y)`.  Drift here
        # means our sliced sprite no longer lands where the engine
        # paints the corresponding tile.
        vp = building_hex_viewpoint(layouts=4, units_per_tile=12.0, dims_x=2, dims_y=1)
        # Even L0 footprint along koord +x: centroid (0.5, 0); slices
        # land symmetric around canvas centre.
        l0 = next(f for f in vp.facings if f.label == "L0_H0")
        cx_l0, cy_l0 = building_footprint_centroid(2, 1, 0)
        anchor_l0 = hex_tile_screen_offset(cx_l0, cy_l0)
        for sl, (x, y) in zip(l0.slices, [(0, 0), (1, 0)], strict=True):
            cell = hex_tile_screen_offset(x, y)
            self.assertEqual(sl.offset, (
                int(round(cell[0] - anchor_l0[0])),
                int(round(cell[1] - anchor_l0[1])),
            ))
        # Odd L1 footprint along koord +y (dims swap): centroid (0, 0.5).
        # Required asymmetric handling -- the legacy "(max-1, max-1)/2"
        # shortcut was correct only for symmetric footprints.
        l1 = next(f for f in vp.facings if f.label == "L1_H0")
        cx_l1, cy_l1 = building_footprint_centroid(2, 1, 1)
        anchor_l1 = hex_tile_screen_offset(cx_l1, cy_l1)
        for sl, (x, y) in zip(l1.slices, [(0, 0), (0, 1)], strict=True):
            cell = hex_tile_screen_offset(x, y)
            self.assertEqual(sl.offset, (
                int(round(cell[0] - anchor_l1[0])),
                int(round(cell[1] - anchor_l1[1])),
            ))


class TestBuildingSquareViewpoint(unittest.TestCase):
    """Square calibration viewpoint: full-canvas Facing per layout
    with per-cell `slices` so the render harness emits both the
    stitched canvas (for the per-layout diff) and the per-tile sprites
    (for the per-cell diff).  Heights > 1 is still unsupported."""

    def test_multi_tile_returns_sliced_layout_facings(self):
        vp = building_square_viewpoint(layouts=4, units_per_tile=12.0, dims_x=2, dims_y=1)
        self.assertEqual(len(vp.facings), 4)
        # canvas = sprite_w * max_dims
        self.assertEqual(vp.canvas_width, 256)
        self.assertEqual(vp.canvas_height, 256)
        # Each layout's Facing carries `slices` listing per-cell screen
        # positions on the 512² canvas, top-down with (0, 0) at the
        # canvas centre.  Even layouts (dims_x=2, dims_y=1) span x;
        # odd layouts swap to span y.
        even = vp.facings[0].slices
        odd = vp.facings[1].slices
        self.assertEqual(
            [sl.label for sl in even], ["L0_Y0_X0_H0", "L0_Y0_X1_H0"],
        )
        self.assertEqual(
            [sl.label for sl in odd], ["L1_Y0_X0_H0", "L1_Y1_X0_H0"],
        )
        # Even-layout cells lie on the (x, x/2) line: koord +x heads SE
        # on the dimetric screen.  Two cells centred at koord ±0.5 land
        # at screen ±(32, 16) from canvas centre.
        self.assertEqual(
            [sl.offset for sl in even], [(-32, -16), (32, 16)],
        )
        # Each slice carries a per-tile pixel-ownership mask (None
        # only in the single-tile fall-through path).
        for sl in even:
            self.assertIsNotNone(sl.alpha_mask)

    def test_single_tile_collapses_to_one_slice_at_origin(self):
        """1×1 footprint: one slice per facing at canvas centre, no
        mask -- the degenerate N-tile case (no neighbours to resolve)."""
        vp = building_square_viewpoint(layouts=4, units_per_tile=12.0, dims_x=1, dims_y=1)
        # canvas = sprite_w * max_dims = 128 for 1×1
        self.assertEqual(vp.canvas_width, DEFAULT_W)
        self.assertEqual(vp.canvas_height, DEFAULT_W)
        for f in vp.facings:
            self.assertEqual(len(f.slices), 1)
            self.assertEqual(f.slices[0].offset, (0, 0))
            self.assertIsNone(f.slices[0].alpha_mask)

    def test_multi_height_doubles_facings_with_z_shift(self):
        """heights nests layouts; each Facing shifts -h *
        sq_height_level_world_z(units_per_tile) in world z so the
        height-h band lands at the camera's z=0 view."""
        from pak.viewpoints import sq_height_level_world_z
        upt = 12.0
        vp = building_square_viewpoint(
            layouts=4, units_per_tile=upt, dims_x=1, dims_y=1, heights=2,
        )
        self.assertEqual(len(vp.facings), 4 * 2)
        for i, f in enumerate(vp.facings):
            l, h = i % 4, i // 4
            self.assertEqual(f.label, f"L{l}_H{h}")
            self.assertEqual(
                f.model_translation,
                (0.0, 0.0, -h * sq_height_level_world_z(upt)),
            )
            self.assertEqual(f.slices[0].label, f"L{l}_Y0_X0_H{h}")


class TestSqTilePixelMask(unittest.TestCase):
    """`sq_tile_pixel_mask` is the dimetric-L1 Voronoi ∩ hex clip that
    keeps multi-tile sprites disjoint — the convention upstream
    pak128.Britain uses for back-to-front paint without overdraw."""

    def test_single_tile_collapses_to_hexagon(self):
        # No neighbours -> only the hex clip applies.  Four corner
        # pixels are outside, the cell centre and ground anchor are in.
        m = sq_tile_pixel_mask((0, 0))
        # Hex corners are clipped (1-px slack absorbs the AA edge ring).
        self.assertEqual(m[0, 0], 0.0)
        self.assertEqual(m[0, DEFAULT_W - 1], 0.0)
        self.assertEqual(m[DEFAULT_W - 1, 0], 0.0)
        self.assertEqual(m[DEFAULT_W - 1, DEFAULT_W - 1], 0.0)
        # Cell centre and ground anchor are inside.
        self.assertEqual(m[DEFAULT_W // 2, DEFAULT_W // 2], 1.0)
        self.assertEqual(m[3 * DEFAULT_W // 4, DEFAULT_W // 2], 1.0)

    def test_adjacent_tiles_disjoint_on_canvas(self):
        # 2x1 footprint, even layout: tile A at (-32, -16) and tile B at
        # (+32, +16) from canvas centre.  Each tile's mask placed at its
        # canvas position must NOT overlap with its neighbour's — the
        # strict-ownership invariant that motivated the whole design.
        import numpy as np
        a_off, b_off = (-32, -16), (32, 16)
        ma = sq_tile_pixel_mask(a_off, [b_off])
        mb = sq_tile_pixel_mask(b_off, [a_off])
        canvas_size = 256
        ca = np.zeros((canvas_size, canvas_size), dtype=np.float32)
        cb = np.zeros((canvas_size, canvas_size), dtype=np.float32)

        def paste(canvas, mask, off):
            cx = canvas_size // 2 + off[0] - DEFAULT_W // 2
            cy = canvas_size // 2 + off[1] - DEFAULT_W // 2
            canvas[cy:cy + DEFAULT_W, cx:cx + DEFAULT_W] = mask
        paste(ca, ma, a_off)
        paste(cb, mb, b_off)
        # Both > 0 anywhere = overlap.
        overlap = ((ca > 0) & (cb > 0)).sum()
        self.assertEqual(overlap, 0)


class TestHexTilePixelMask(unittest.TestCase):
    """`hex_tile_pixel_mask` is the world-Euclidean Voronoi ∩ projected-
    hex clip that keeps multi-tile hex sprites disjoint.  Hex-lattice
    neighbours adjacent in `HEX_KOORD_*_WORLD` must produce a clean
    edge cut; the projected hex shape clips an isolated tile."""

    def test_single_tile_collapses_to_hex(self):
        m = hex_tile_pixel_mask((0, 0))
        # All four sprite corners sit outside the projected hex (anchor
        # at (W/2, 3W/4), hex spans dy ∈ [-W/4, +W/4]).
        self.assertEqual(m[0, 0], 0.0)
        self.assertEqual(m[0, DEFAULT_W - 1], 0.0)
        self.assertEqual(m[DEFAULT_W - 1, 0], 0.0)
        self.assertEqual(m[DEFAULT_W - 1, DEFAULT_W - 1], 0.0)
        # Anchor + sprite centre inside; E/W hex tips inside one pixel.
        self.assertEqual(m[3 * DEFAULT_W // 4, DEFAULT_W // 2], 1.0)
        self.assertEqual(m[DEFAULT_W // 2, DEFAULT_W // 2], 1.0)
        self.assertEqual(m[3 * DEFAULT_W // 4, DEFAULT_W - 2], 1.0)
        self.assertEqual(m[3 * DEFAULT_W // 4, 1], 1.0)

    def test_adjacent_tiles_disjoint_on_canvas(self):
        # 2x1 footprint along koord+x.  Tile B is one `HEX_KOORD_Q_
        # WORLD` step from A on screen — their projected hexes meet
        # along a shared edge, must partition the canvas with no
        # overlap once pasted at their respective slots.
        import numpy as np
        a_off, b_off = (-48, -16), (48, 16)
        ma = hex_tile_pixel_mask(a_off, [b_off])
        mb = hex_tile_pixel_mask(b_off, [a_off])
        canvas_size = 256
        ca = np.zeros((canvas_size, canvas_size), dtype=np.float32)
        cb = np.zeros((canvas_size, canvas_size), dtype=np.float32)

        def paste(canvas, mask, off):
            cx = canvas_size // 2 + off[0] - DEFAULT_W // 2
            cy = canvas_size // 2 + off[1] - DEFAULT_W // 2
            canvas[cy:cy + DEFAULT_W, cx:cx + DEFAULT_W] = mask
        paste(ca, ma, a_off)
        paste(cb, mb, b_off)
        overlap = ((ca > 0) & (cb > 0)).sum()
        self.assertEqual(overlap, 0)

    def test_ring_voronoi_contained_in_cell_shape(self):
        # The projected hex cell-shape coincides with the Voronoi cell
        # against the six hex-lattice neighbours, so adding all six as
        # `other_offsets` can only shrink the mask -- never grow it.
        # Strict equality fails on the +1 AA slack ring and on the
        # closer-to-viewer tie-break, so containment is the invariant.
        import numpy as np
        neighbours = [
            (int(round(x)), int(round(y)))
            for x, y in (hex_tile_screen_offset(qx, ry)
                         for qx, ry in [(1, 0), (0, 1), (-1, 1),
                                        (-1, 0), (0, -1), (1, -1)])
        ]
        m_ring = hex_tile_pixel_mask((0, 0), neighbours)
        m_solo = hex_tile_pixel_mask((0, 0))
        self.assertTrue(np.all(m_ring <= m_solo))
        # Bulk of the cell-shape (well inside the strict hex) survives
        # the ring cut -- not all of m_solo is slack.
        self.assertGreater(m_ring.sum(), 0.9 * m_solo.sum())


class TestViewpointPickleRoundTrip(unittest.TestCase):
    """`pak.bake.run_render` marshals every Viewpoint across the
    subprocess boundary as a pickle.  Lambdas / inline closures in the
    `camera_ortho` / `sun_energy` / `fit_matrix` fields break that
    silently -- subprocess fails after the pickle load on a "can't
    pickle local object" -- so pin the round-trip here.  Add new
    factories to this list; cost is one line per factory."""

    def _assert_round_trip(self, vp):
        import pickle
        vp2 = pickle.loads(pickle.dumps(vp))
        a = BlendAuthored(ortho_scale=12.0, sun_energy=0.028)
        self.assertEqual(vp2.camera_ortho(a), vp.camera_ortho(a))
        self.assertEqual(vp2.sun_energy(a), vp.sun_energy(a))
        self.assertEqual(vp2.fit_matrix(a), vp.fit_matrix(a))

    def test_singletons(self):
        self._assert_round_trip(HEX_VIEWPOINT)
        self._assert_round_trip(SQUARE_VIEWPOINT)

    def test_factories(self):
        lighting = Lighting(
            world_ambient=(0.5, 0.5, 0.5), sun_energy_scale=1.5,
            sun_elev_deg=45.0, sun_az_offset_deg=-90.0,
        )
        for vp in [
            building_hex_viewpoint(layouts=2, units_per_tile=12.0,
                                   dims_x=2, dims_y=1, lighting=lighting),
            building_square_viewpoint(layouts=2, units_per_tile=12.0),
            bridge_hex_viewpoint("image"),
            bridge_square_viewpoint(),
            tree_hex_viewpoint(ages=4, seasons=1),
            tree_square_viewpoint(ages=4, seasons=1),
            fence_square_viewpoint(),
            tunnel_hex_viewpoint(),
            tunnel_square_viewpoint(),
        ]:
            self._assert_round_trip(vp)


if __name__ == "__main__":
    unittest.main()
