"""Tests for `pak.viewpoints` -- the per-camera + per-viewpoint helpers
shared by hex and square render paths.

Run from the repo root:

    python3 -m unittest tests.test_viewpoints
"""

from __future__ import annotations

import math
import unittest

from pak.viewpoints import (
    HEX_VIEWPOINT,
    SQUARE_VIEWPOINT,
    building_hex_viewpoint,
    building_square_viewpoint,
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
        self.assertEqual(SQUARE_VIEWPOINT.engine, "CYCLES")
        self.assertEqual(HEX_VIEWPOINT.engine, "CYCLES")
        self.assertEqual(building_square_viewpoint(layouts=4).engine,
                         "BLENDER_EEVEE")
        self.assertEqual(building_hex_viewpoint(layouts=6, dims_x=1, dims_y=1).engine,
                         "BLENDER_EEVEE")


if __name__ == "__main__":
    unittest.main()
