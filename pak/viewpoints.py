"""Viewpoint definitions for the unified renderer (`render.py`).

Two viewpoints ship as constants:

- `SQUARE_VIEWPOINT` reproduces the upstream
  `render_SimutransRender_pak128Britain-65.py` "vehicles"-alignment
  setup verbatim (8 cameras around the asset, ortho_scale=24, sun
  rotating with the camera).  Used by `diff_upstream.py` to validate
  the renderer against the published pak PNGs.

- `HEX_VIEWPOINT` is this project's hex projection for vehicles: one
  fixed camera looking +Y, one fixed world sun, mesh pre-sheared via
  the `hex_proj_shear()` extrinsic.  Per-facing variation is in the
  mesh's Z rotation, not the camera.

Plus one viewpoint factory:

- `building_hex_viewpoint(layouts, dims_x, dims_y)` returns a hex
  Viewpoint with one Facing per `(layout, y, x)` cell of a multi-
  tile building's footprint.  The cell's koord-(x,y) offset from
  the building origin is converted to a world translation via the
  hex tile lattice (see `HEX_KOORD_Q_WORLD` / `_R_WORLD` below) and
  baked into the Facing's `model_translation`, so the standard hex
  camera renders each cell with that tile at world origin.  Layout
  rotation is `90° * l` CCW; this is a guess at the engine's layout-
  to-screen-rotation convention and the first real bake will pin
  the sign.

All three feed the same `render_atlas()` pipeline; the only
difference is which `Viewpoint` instance gets passed in.
"""

from __future__ import annotations

import math
from math import radians

from pak.hex_synth import DEFAULT_W, HEX_TILE_RADIUS, UPSTREAM_ORTHO_SCALE, hex_proj_shear
from pak.render import Facing, Viewpoint


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


# === Square-dimetric, normal alignment (4 cardinal cameras) ===============
#
# Buildings (stops, signals, road vehicles) render under upstream's
# "normal alignment" rather than "vehicles alignment"; the cameras sit
# further out and at slightly different angles so a building's ground
# line lands on the tile's lower edge.  Lifted verbatim from
# `render_SimutransRender_pak128Britain-65.py`'s `op_list == "0"` branch
# (the 4-view normal-alignment renderer for cardinal-only assets like
# 4-layout buildings).  Same cam rot_x=60, ortho_scale=24, sun rot_x=90
# as `_UPSTREAM`; only `cam.location` differs from the vehicles list.
#
# 4-view rather than 8-view because the only ported asset class is
# 4-layout buildings; the 8-view normal cameras for road vehicles
# follow the same convention with the diagonal positions added.

# (label, cam_rot_z_deg, location_normal_alignment, sun_rot_z_deg)
_UPSTREAM_NORMAL_CARDINAL = [
    ("S",   45, ( 10.0, -10.0, 11.6),  90),
    ("W",  135, ( 10.0,  10.0, 11.6), 180),
    ("N",  225, (-10.0,  10.0, 11.6), 270),
    ("E",  315, (-10.0, -10.0, 11.6),   0),
]


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


# === Multi-tile building viewpoint factory ================================
#
# The hex tile lattice in world coords — koord +x (+q in hex_proj.h's
# axial naming) heads SE, koord +y (+r) heads S.  Derivation: invert
# `display/hex_proj.h::hex_screen_dx/dy` (which give pixel offsets for
# axial deltas) against the camera's world→screen mapping at
# `ortho_scale = 2R`, `W = 128`.  A koord +x step yields screen
# (3W/4, W/4) = world (3R/2, -R·√3/2); a koord +y step yields screen
# (0, W/2) = world (0, -R·√3).  Bake-side single source of truth for
# multi-tile footprint translations.

_SQRT2 = math.sqrt(2.0)
_SQRT3 = math.sqrt(3.0)

HEX_KOORD_Q_WORLD: tuple[float, float] = (1.5 * HEX_TILE_RADIUS,
                                          -0.5 * _SQRT3 * HEX_TILE_RADIUS)
HEX_KOORD_R_WORLD: tuple[float, float] = (0.0,
                                          -_SQRT3 * HEX_TILE_RADIUS)


# World-z (intra-tile) shift per `backimage[…][height][…]` level.
# The engine paints level h at `ypos -= h * raster_width` screen px
# (`obj/gebaeude.cc::display`); at the standard `raster_width = W`
# and the hex projection's `ortho_scale = 2R`, one full image height
# = 2 intra-tile units of post-shear y.  Under the `hex_proj_shear`
# z-coefficient `√2`, that's `2/√2 = √2` intra-tile in world z.
# Bake side translates the model DOWN by `h * HEX_HEIGHT_LEVEL_WORLD_Z`
# to render the height-h slice into the (un-shifted) hex camera; the
# engine then paints each level at its proper screen offset.
HEX_HEIGHT_LEVEL_WORLD_Z: float = _SQRT2 * HEX_TILE_RADIUS


def hex_tile_world_offset(qx: int, ry: int) -> tuple[float, float]:
    """World (x, y) of tile (qx, ry) relative to the koord origin.

    The lattice basis is `HEX_KOORD_Q_WORLD` (koord +x) and
    `HEX_KOORD_R_WORLD` (koord +y).  Bake side passes the negative
    of this as the per-cell `model_translation` so each rendered
    tile centres on world origin under the standard hex camera."""
    return (qx * HEX_KOORD_Q_WORLD[0] + ry * HEX_KOORD_R_WORLD[0],
            qx * HEX_KOORD_Q_WORLD[1] + ry * HEX_KOORD_R_WORLD[1])


def building_square_viewpoint(
    layouts: int, dims_x: int = 1, dims_y: int = 1, heights: int = 1,
) -> Viewpoint:
    """Square-dimetric Viewpoint mirroring `building_square_viewpoint`'s
    role for the calibration diff: one Facing per `(l, y, x, h)` cell
    in `iter_building_cells` order, rendered under upstream's normal-
    alignment cardinal cameras instead of the hex camera.

    Layout `l` selects one of the four cardinal cameras
    (S, W, N, E in `_UPSTREAM_NORMAL_CARDINAL`) — equivalent to upstream
    rotating the camera around the unrotated model, rather than rotating
    the model under a fixed camera the way `building_hex_viewpoint`
    does.  The two conventions render the same silhouette per layout,
    but only the camera-rotation form matches upstream's actually-
    published per-layout PNGs (which is what the diff measures against).

    `fit_kind="none"` renders at the blend's authored ortho_scale, so
    the result is directly comparable to upstream's published cells
    (which are at the same blend-native scale).

    Today this only supports `dims_x == dims_y == heights == 1`; multi-
    tile per-cell translation would need a square tile lattice
    analogous to `HEX_KOORD_Q_WORLD` / `_R_WORLD`, which is deferred
    until a multi-tile building actually ports.  Raises on those cases
    so a future caller can't silently get layout-only diffs back when
    they wanted per-cell.
    """
    if dims_x != 1 or dims_y != 1 or heights != 1:
        raise NotImplementedError(
            "square_building viewpoint is single-tile single-height only; "
            "multi-tile diffs need a square tile lattice (deferred)"
        )
    if layouts > len(_UPSTREAM_NORMAL_CARDINAL):
        raise ValueError(
            f"square_building supports up to {len(_UPSTREAM_NORMAL_CARDINAL)} "
            f"layouts (cardinal cameras); got {layouts}"
        )
    facings: list[Facing] = []
    for l in range(layouts):
        label, cam_z, loc, sun_z = _UPSTREAM_NORMAL_CARDINAL[l]
        facings.append(Facing(
            label=f"L{l}_Y0_X0_H0",
            camera_location=loc,
            camera_rotation_euler=(radians(60), 0.0, radians(cam_z)),
            sun_rotation_euler=(radians(90), 0.0, radians(sun_z)),
            model_rot_z_deg=0.0,
        ))
    return Viewpoint(
        name="square_building",
        image_width=DEFAULT_W,
        # `None` => use the blend's authored ortho_scale.  Buildings are
        # typically authored at 12 (twice the per-cell zoom vs vehicles'
        # 24); honouring that is what makes the diff align with
        # upstream's actually-published per-blend renders.
        ortho_scale=None,
        sun_energy=_SUN_ENERGY,
        fit_kind="none",
        extrinsic=None,
        facings=facings,
    )


def building_hex_viewpoint(
    layouts: int, dims_x: int, dims_y: int, heights: int = 1,
) -> Viewpoint:
    """Hex Viewpoint for a multi-tile building of footprint `dims_x × dims_y`
    with `layouts` rotation variants and `heights` vertical-stack
    cells.

    Builds one Facing per `(layout, y, x, height)` quadruple in the
    canonical `pak.dat.iter_building_cells` order — even layouts
    iterate `y in [0, dims_y), x in [0, dims_x)`; odd layouts swap
    to `y in [0, dims_x), x in [0, dims_y)`, mirroring the engine's
    `h = (l & 1) ? size.x : size.y` rule in `building_writer.cc`.
    Each Facing's `model_translation` carries the tile's negated
    world XY centre (`hex_tile_world_offset(qx=x, ry=y)`, after
    fit-scale so the camera at origin renders that tile's content)
    plus a Z shift of `-height * HEX_HEIGHT_LEVEL_WORLD_Z` — drops
    the model down so the height-h slice falls into the hex camera's
    visible window.  Layout `l` rotates the model by `90° * l` CCW
    around Z — the engine's layout-to-map-rotation convention is
    unverified here; if a port shows wrong rotations, flip the sign
    or shift the modulus.
    """
    facings: list[Facing] = []
    for l in range(layouts):
        if l & 1:
            yh, xw = dims_x, dims_y
        else:
            yh, xw = dims_y, dims_x
        for y in range(yh):
            for x in range(xw):
                for h in range(heights):
                    wx, wy = hex_tile_world_offset(qx=x, ry=y)
                    facings.append(Facing(
                        label=f"L{l}_Y{y}_X{x}_H{h}",
                        camera_location=_HEX_CAM_LOC,
                        camera_rotation_euler=_HEX_CAM_ROT,
                        sun_rotation_euler=_HEX_SUN_ROT,
                        model_rot_z_deg=90.0 * l,
                        model_translation=(-wx, -wy,
                                           -h * HEX_HEIGHT_LEVEL_WORLD_Z),
                    ))
    return Viewpoint(
        name="hex_building",
        image_width=DEFAULT_W,
        ortho_scale=2.0 * HEX_TILE_RADIUS,
        sun_energy=_SUN_ENERGY,
        fit_kind="hex",
        extrinsic=hex_proj_shear(),
        facings=facings,
    )
