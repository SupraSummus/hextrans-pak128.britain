"""Viewpoint definitions for the unified renderer (`render.py`).

Two viewpoints ship:

- `SQUARE_VIEWPOINT` reproduces the upstream
  `render_SimutransRender_pak128Britain-65.py` "vehicles"-alignment
  setup verbatim (8 cameras around the asset, ortho_scale=24, sun
  rotating with the camera).  Used by `diff_upstream.py` to validate
  the renderer against the published pak PNGs.

- `HEX_VIEWPOINT` is this project's hex projection: one fixed camera
  looking +Y, one fixed world sun, mesh pre-sheared via the
  `hex_proj_shear()` extrinsic.  Per-facing variation is in the mesh's
  Z rotation, not the camera.

Both viewpoints feed the same `render_atlas()` pipeline; the only
difference is which `Viewpoint` instance gets passed in.
"""

from __future__ import annotations

from math import radians

from hex_synth import DEFAULT_W, HEX_TILE_RADIUS, UPSTREAM_ORTHO_SCALE, hex_proj_shear
from render import Facing, Viewpoint


# Upstream sun lamp energy, from Lamp.001 in the Britain blends.  Matching
# this keeps the calibration diff's mean|dRGB| meaningful -- a different
# energy would shift every rendered pixel and inflate the residual without
# implying real drift.
_SUN_ENERGY = 0.028


# === Square-dimetric (upstream) ===========================================
#
# Per-facing camera and sun parameters lifted verbatim from
# `render_SimutransRender_pak128Britain-65.py`'s SCENE_OT_simurender_render_views.
# The "vehicles" alignment (`loc_v`) is the right choice for trains,
# trams, ships and aircraft per CLAUDE.md's calibration contract; static
# scenery uses "bases" alignment, not modelled here yet.  All cameras
# share `(rot_x=60deg, rot_y=0)` and `ortho_scale=24`; all suns share
# `(rot_x=90deg, rot_y=0)`.  The per-facing axial rotations follow:

# (label, cam_rot_z_deg, location_vehicles_alignment, sun_rot_z_deg)
_UPSTREAM = [
    ("S",   45,  ( 6.6,   -7.9,   11.6),  90),
    ("SW",  90,  ( 7.5,    0.6,   10.0), 135),
    ("W",  135,  ( 6.72,   8.2,   11.6), 180),
    ("NW", 180,  ( 0.0,   14.14,  11.6), 225),
    ("N",  225,  (-7.0,    8.5,   11.6), 270),
    ("NE", 270,  (-10.3,  -0.75,  11.6), 315),
    ("E",  315,  (-32.6, -33.6,   32.5),   0),
    ("SE", 360,  ( 0.0,  -11.0,   11.6),  45),
]


SQUARE_VIEWPOINT = Viewpoint(
    name="square",
    image_width=DEFAULT_W,
    ortho_scale=UPSTREAM_ORTHO_SCALE,
    sun_energy=_SUN_ENERGY,
    fit_kind="none",
    extrinsic=None,
    facings=[
        Facing(
            label=label,
            camera_location=loc,
            camera_rotation_euler=(radians(60), 0.0, radians(cam_z)),
            sun_rotation_euler=(radians(90), 0.0, radians(sun_z)),
            model_rot_z_deg=0.0,
        )
        for label, cam_z, loc, sun_z in _UPSTREAM
    ],
)


# === Hex projection =======================================================
#
# One fixed camera looking +Y at the origin, ortho_scale=2R so world
# x in [-R, R] maps to the image's full width.  Camera lifted by 0.5
# so world z=0 lands at pixel row 96 of the 128-tall image (leaving
# 64 px of top headroom for z-lifted geometry).  Sun pinned at south +
# 60deg elevation in world space.  Per-facing variation lives in the
# mesh's Z rotation, baked together with the projection shear via
# `mesh.transform()` (see render.py and CLAUDE.md -> "matrix_basis
# drops shear").

_HEX_CAM_LOC = (0.0, -10.0, 0.5)
_HEX_CAM_ROT = (radians(90), 0.0, 0.0)
_HEX_SUN_ROT = (radians(30), 0.0, 0.0)


# Same direction labels as the square viewpoint so .dat keys port
# without facing relabelling.
_HEX_FACINGS = [
    ("S",     0),
    ("SW",   45),
    ("W",    90),
    ("NW",  135),
    ("N",   180),
    ("NE",  225),
    ("E",   270),
    ("SE",  315),
]


HEX_VIEWPOINT = Viewpoint(
    name="hex",
    image_width=DEFAULT_W,
    ortho_scale=2.0 * HEX_TILE_RADIUS,
    sun_energy=_SUN_ENERGY,
    fit_kind="hex",
    extrinsic=hex_proj_shear(),
    facings=[
        Facing(
            label=label,
            camera_location=_HEX_CAM_LOC,
            camera_rotation_euler=_HEX_CAM_ROT,
            sun_rotation_euler=_HEX_SUN_ROT,
            model_rot_z_deg=rot,
        )
        for label, rot in _HEX_FACINGS
    ],
)
