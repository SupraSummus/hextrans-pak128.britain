"""Tests for `pak.viewpoints` -- the per-camera + per-viewpoint helpers
shared by hex and square render paths.

Run from the repo root:

    python3 -m unittest tests.test_viewpoints
"""

from __future__ import annotations

import math
import unittest

from pak.render import CYCLES, EEVEE, BlendAuthored
from pak.viewpoints import (
    DEFAULT_W,
    HEX_VIEWPOINT,
    SQUARE_VIEWPOINT,
    building_hex_viewpoint,
    building_square_viewpoint,
    hex_tile_screen_offset,
    sq_tile_pixel_mask,
    sun_rotation_for_camera,
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
        vp = building_square_viewpoint(layouts=4)
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
        vp = building_hex_viewpoint(layouts=6, dims_x=1, dims_y=1)
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
        self.assertIs(building_square_viewpoint(layouts=4).engine, EEVEE)
        self.assertIs(building_hex_viewpoint(layouts=6, dims_x=1, dims_y=1).engine,
                      EEVEE)


class TestBuildingHexMultiTile(unittest.TestCase):
    """Multi-tile path in `building_hex_viewpoint`: one Facing per
    (layout, height) with N=dims_x*dims_y slices at hex koord screen
    positions.  Catches structural drift in the slice-list generation
    that would silently scramble the atlas's per-cell labels."""

    def test_single_tile_path_uses_no_slices(self):
        # Backwards compatibility lock: dims=(1,1) keeps the legacy
        # 1-cell-per-facing structure (no slicing), no canvas override.
        vp = building_hex_viewpoint(layouts=6, dims_x=1, dims_y=1)
        self.assertEqual(len(vp.facings), 6)
        self.assertIsNone(vp.canvas_width)
        self.assertIsNone(vp.canvas_height)
        for f in vp.facings:
            self.assertIsNone(f.slices)

    def test_multi_tile_emits_one_facing_per_layout_with_slices(self):
        # 2x1x4 (mechanical-signalbox-large shape): 4 layouts × 1 height
        # = 4 facings; each carries 2 slices (the per-layout cell count
        # under iter_building_cells, regardless of even/odd swap).
        vp = building_hex_viewpoint(layouts=4, dims_x=2, dims_y=1)
        self.assertEqual(len(vp.facings), 4)
        for f in vp.facings:
            self.assertIsNotNone(f.slices)
            self.assertEqual(len(f.slices), 2)
        self.assertGreater(vp.canvas_width, DEFAULT_W)

    def test_multi_tile_fit_matrix_doubles_scale_vs_single(self):
        # Multi-tile blends are authored at `ortho = max(dims) ·
        # per-tile-ortho`; the fit divisor `max(dims)` should produce
        # exactly twice the scale of the single-tile fit at the same
        # authored ortho (matching the previous `fit_ortho_divisor=2.0`
        # state pin for a 2x1 footprint).
        authored = BlendAuthored(ortho_scale=12.0)
        single = building_hex_viewpoint(layouts=6, dims_x=1, dims_y=1)
        multi = building_hex_viewpoint(layouts=4, dims_x=2, dims_y=1)
        s = single.fit_matrix(authored)[0][0]
        m = multi.fit_matrix(authored)[0][0]
        self.assertAlmostEqual(m, 2 * s, places=6)

    def test_ortho_per_tile_pins_scale_regardless_of_authored(self):
        # When `ortho_per_tile` is set, fit_matrix returns a constant
        # scale of `2R / (per_tile * max_dims)` independent of the
        # blend's authored ortho_scale.  Replaces the previous
        # render-time `fit_ortho_per_tile` recomputation.
        vp = building_hex_viewpoint(
            layouts=4, dims_x=2, dims_y=2, ortho_per_tile=24.0,
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
        vp = building_hex_viewpoint(layouts=4, dims_x=2, dims_y=1)
        labels_per_layout = {f.label: [s[0] for s in f.slices]
                             for f in vp.facings}
        self.assertEqual(labels_per_layout["L0_H0"],
                         ["L0_Y0_X0_H0", "L0_Y0_X1_H0"])
        # L=1 swap: y iterates over dims_x=2, x over dims_y=1.
        self.assertEqual(labels_per_layout["L1_H0"],
                         ["L1_Y0_X0_H0", "L1_Y1_X0_H0"])

    def test_multi_tile_slice_centres_match_hex_screen_lattice(self):
        # The slice offsets must reproduce the engine's per-tile
        # screen positions: `hex_tile_screen_offset(qx=x, ry=y)` shifted
        # to centre the multi-tile footprint in the canvas.  Drift
        # here means our sliced sprite no longer lands where the
        # engine paints the corresponding tile.
        vp = building_hex_viewpoint(layouts=4, dims_x=2, dims_y=1)
        l0 = next(f for f in vp.facings if f.label == "L0_H0")
        # Even layout iterates (y=0, x in [0, 1]).  Centring offset
        # subtracts cx_max/2, cy_max/2 from the raw koord-screen
        # position (cx_max/cy_max = hex offset of the worst-case koord).
        cx_max, cy_max = hex_tile_screen_offset(max(2, 1) - 1, max(2, 1) - 1)
        expected = [
            hex_tile_screen_offset(0, 0),
            hex_tile_screen_offset(1, 0),
        ]
        for sl, (want_cx, want_cy) in zip(l0.slices, expected, strict=True):
            self.assertEqual(sl.offset, (int(round(want_cx - cx_max / 2)),
                                         int(round(want_cy - cy_max / 2))))


class TestBuildingSquareViewpoint(unittest.TestCase):
    """Square calibration viewpoint supports multi-tile via a wider
    full-canvas Facing per layout, with per-cell `slices` so the render
    harness emits both the stitched canvas (for the per-layout diff)
    and the per-tile sprites (for the per-cell diff).  Heights > 1
    is still unsupported."""

    def test_multi_tile_returns_sliced_layout_facings(self):
        vp = building_square_viewpoint(layouts=4, dims_x=2, dims_y=1)
        self.assertEqual(len(vp.facings), 4)
        # Multi-tile: canvas widened to 512x512.
        self.assertEqual(vp.canvas_width, 512)
        self.assertEqual(vp.canvas_height, 512)
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

    def test_single_tile_no_slices(self):
        """Legacy 1-cell-per-facing path still kicks in for dims=(1, 1)."""
        vp = building_square_viewpoint(layouts=4, dims_x=1, dims_y=1)
        for f in vp.facings:
            self.assertIsNone(f.slices)
        self.assertIsNone(vp.canvas_width)
        self.assertIsNone(vp.canvas_height)

    def test_multi_height_raises(self):
        with self.assertRaises(NotImplementedError):
            building_square_viewpoint(layouts=4, dims_x=1, dims_y=1, heights=2)


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


if __name__ == "__main__":
    unittest.main()
