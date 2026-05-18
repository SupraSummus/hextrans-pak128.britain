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

from pak.hex_synth import (
    DEFAULT_W,
    HEX_SHEAR_Z_COEF,
    HEX_TILE_RADIUS,
    UPSTREAM_ORTHO_SCALE,
    hex_proj_shear,
)
from pak.render import Facing, Viewpoint

# Upstream sun lamp energy, from Lamp.001 in the Britain blends.  Matching
# this keeps the calibration diff's mean|dRGB| meaningful -- a different
# energy would shift every rendered pixel and inflate the residual without
# implying real drift.  This value was authored for Blender Internal where
# 0.028 was a reasonable directional contribution on top of ambient ~0.3;
# Cycles + EEVEE interpret "energy" in W/m^2-ish units where 0.028 ≈ zero.
_SUN_ENERGY = 0.028

# Engine-substitution scale: BI's 0.028 sun energy reads as near-zero
# under EEVEE's PBR pipeline, so the EEVEE buildings path multiplies
# the .blend's authored value by this factor.  Empirically 2.0/0.028
# (= ~71.4) gives a comparable apparent brightness on `res_1600_kg_01`
# vs the upstream-published PNG; this is the only post-extraction
# magic number in the building lighting path.
_BI_TO_EEVEE_SUN_SCALE = 2.0 / _SUN_ENERGY


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

# (label, cam_rot_z_deg, location_normal_alignment).  Sun rotation is
# derived from cam_z by `sun_rotation_for_camera` — single source of
# truth shared with the hex building viewpoint, so the same
# upstream-calibrated "front-left lit at 60° elev" convention applies
# to both the apples-to-apples diff and the shipped atlas.
_UPSTREAM_NORMAL_CARDINAL = [
    ("S",   45, ( 10.0, -10.0, 11.6)),
    ("W",  135, ( 10.0,  10.0, 11.6)),
    ("N",  225, (-10.0,  10.0, 11.6)),
    ("E",  315, (-10.0, -10.0, 11.6)),
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
# Vehicles & ways: sun south at 60° elevation, matching `pak.hex_synth`'s
# pak-wide `SUN_DIR`.  Buildings use `sun_rotation_for_camera` instead.
_HEX_SUN_ROT = (radians(30), 0.0, 0.0)


def sun_rotation_for_camera(
    cam_z_deg: float,
    sun_elev_deg: float = 30.0,
    sun_az_offset_deg: float = -90.0,
) -> tuple[float, float, float]:
    """Sun rotation_euler that puts the sun at `sun_az_offset_deg` from
    the camera's screen-direction at `sun_elev_deg` elevation.

    Blender's SUN lamp emits in its local -Z axis: rotation_x=0 means
    straight-down (90° elev), rotation_x=90° means horizontal (0° elev).
    Sun_z = cam_z + az_offset places the sun screen-relative.

    Defaults are calibrated to EEVEE-substituted output, not literal
    BI convention.  Upstream's `render_SimutransRender_pak128Britain-65
    .py` hardcodes (elev=0°, az_offset=+45°) for the BI-era pipeline;
    that same direction under EEVEE produces a visibly worse match to
    the upstream PNG (mean |dRGB| 45 vs 34 for `res_1600_kg_01`) because
    EEVEE's PBR lighting interprets a horizontal sun differently from
    BI's flat-Lambert model.  The (elev=30°, az=-90°) defaults are
    the EEVEE-substitution find that best approximates the BI-rendered
    upstream PNG.  See CLAUDE.md → "Building-bake architecture"."""
    return (radians(90.0 - sun_elev_deg), 0.0,
            radians(cam_z_deg + sun_az_offset_deg))


# Hex camera doesn't rotate per facing (the model rotates under it), so
# cam_z=0 across every hex Facing.
_HEX_BUILDING_SUN_ROT = sun_rotation_for_camera(cam_z_deg=0.0)


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

_SQRT3 = math.sqrt(3.0)

HEX_KOORD_Q_WORLD: tuple[float, float] = (1.5 * HEX_TILE_RADIUS,
                                          -0.5 * _SQRT3 * HEX_TILE_RADIUS)
HEX_KOORD_R_WORLD: tuple[float, float] = (0.0,
                                          -_SQRT3 * HEX_TILE_RADIUS)


# World-z (intra-tile) shift per `backimage[…][height][…]` level.
# The engine paints level h at `ypos -= h * raster_width` screen px
# (`obj/gebaeude.cc::display`); at the standard `raster_width = W`
# and the hex projection's `ortho_scale = 2R`, one full image height
# = 2R intra-tile units of post-shear y.  Bake side translates the
# model DOWN by `h * HEX_HEIGHT_LEVEL_WORLD_Z` (= `2R / shear_z_coef`)
# in world z to render the height-h slice into the (un-shifted) hex
# camera; the engine then paints each level at its proper screen
# offset.
HEX_HEIGHT_LEVEL_WORLD_Z: float = 2.0 * HEX_TILE_RADIUS / HEX_SHEAR_Z_COEF


def hex_tile_world_offset(qx: int, ry: int) -> tuple[float, float]:
    """World (x, y) of tile (qx, ry) relative to the koord origin.

    The lattice basis is `HEX_KOORD_Q_WORLD` (koord +x) and
    `HEX_KOORD_R_WORLD` (koord +y).  Bake side passes the negative
    of this as the per-cell `model_translation` so each rendered
    tile centres on world origin under the standard hex camera."""
    return (qx * HEX_KOORD_Q_WORLD[0] + ry * HEX_KOORD_R_WORLD[0],
            qx * HEX_KOORD_Q_WORLD[1] + ry * HEX_KOORD_R_WORLD[1])


def hex_tile_screen_offset(qx: int, ry: int) -> tuple[float, float]:
    """Image-space pixel offset for tile `(qx, ry)` under the standard
    hex camera (`ortho_scale=2R`, image width `DEFAULT_W`).

    Derivation: world `(1.5·R·qx, -√3/2·R·qx - √3·R·ry, 0)` projects to
    screen `(W/(2R)·wx, -W/(2R·√3)·wy)` under `hex_proj_shear`.
    Substituting and flipping y for top-down image coords gives:

        cx_px = 0.75 · W · qx
        cy_px = 0.25 · W · qx + 0.5 · W · ry

    Used by `building_hex_viewpoint` for multi-tile slice centring."""
    return (0.75 * DEFAULT_W * qx,
            0.25 * DEFAULT_W * qx + 0.5 * DEFAULT_W * ry)


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
    tile calibration against the shipped 4x4 atlas is deferred because
    upstream's published per-cell PNGs come out of a hidden assembly
    stage (per-cardinal full-canvas renders -> crop/arrange into the
    final 4xN grid) that doesn't ship with the blends repo, so the
    target itself isn't reproducible from public artifacts.  See
    TODO.md -> "Multi-tile building port".
    """
    if dims_x != 1 or dims_y != 1 or heights != 1:
        raise NotImplementedError(
            "square_building viewpoint is single-tile single-height only; "
            "multi-tile calibration target is upstream-private (see TODO.md)"
        )
    if layouts > len(_UPSTREAM_NORMAL_CARDINAL):
        raise ValueError(
            f"square_building supports up to {len(_UPSTREAM_NORMAL_CARDINAL)} "
            f"layouts (cardinal cameras); got {layouts}"
        )
    facings: list[Facing] = []
    for l in range(layouts):
        label, cam_z, loc = _UPSTREAM_NORMAL_CARDINAL[l]
        facings.append(Facing(
            label=f"L{l}_Y0_X0_H0",
            camera_location=loc,
            camera_rotation_euler=(radians(60), 0.0, radians(cam_z)),
            sun_rotation_euler=sun_rotation_for_camera(cam_z),
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
        # `None` => use the blend's authored sun energy (0.028 in
        # Britain blends) scaled by `_BI_TO_EEVEE_SUN_SCALE`.
        sun_energy=None,
        sun_energy_scale=_BI_TO_EEVEE_SUN_SCALE,
        fit_kind="none",
        extrinsic=None,
        facings=facings,
        engine="BLENDER_EEVEE",
    )


def bridge_hex_viewpoint() -> Viewpoint:
    """Hex Viewpoint for the JH bridge blends — quick-and-dirty port of
    `bridge_square_viewpoint` onto the hex camera + hex shear.

    Renders all 8 hex facings (S/SW/W/NW/N/NE/E/SE) through the
    project's standard hex camera with the same way-material strip
    rules as the square probe.  Bridge geometry is z-shifted up by
    `HEX_HEIGHT_LEVEL_WORLD_Z` so the deck sits where the engine
    expects elevated way geometry — same shift `building_hex_viewpoint`
    uses for the `height` axis.  No cell-anchoring beyond that yet;
    this is "show what the blend looks like under hex projection",
    not a calibrated bridge bake.
    """
    return Viewpoint(
        name="bridge_hex",
        image_width=DEFAULT_W,
        ortho_scale=2.0 * HEX_TILE_RADIUS,
        sun_energy=_SUN_ENERGY,
        sun_energy_scale=1.0,
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
        strip_meshes=("Sphere", "Plane.005", "Plane.007"),
        strip_material_substrings=(
            "Rail", "Chair", "Wood", "Ballast", "Tarmac",
        ),
    )


def bridge_square_viewpoint() -> Viewpoint:
    """4-cardinal Viewpoint for the JamesHood bridge blends (e.g.
    `ways/plate_girder/straight.blend`).

    JH bridge blends ship one ORTHO camera at the upstream normal-
    alignment "E" slot `(-10, -10, 11.6)` with `ortho_scale=12.0` —
    same convention as buildings/fence rather than the vehicle path's
    pinned 24.  Use the blend's authored ortho_scale (`None` here):
    bridges in upstream are rendered at "building scale" so a single
    span fills the cell width (`Back[NS]` measures 104 px wide on the
    128 px cell, matching JH's 9 world unit bridge at ortho=12).  The
    `,0,32` y-shift on every `BackImage` / `FrontImage` line in the dat
    is a runtime draw offset — both upstream and our sprite content
    share it, so the diff itself doesn't see that offset.

    Strip the way (rails, sleepers, chairs, ballast, road tarmac) by
    material-substring match — `Rail` / `Chair` / `Wood` (sleepers) /
    `Ballast` / `Tarmac` — and the two authoring-context planes
    `Plane.005` (an 8×8 ground reference) + `Plane.007` (a 5.5×8.3
    backdrop) by name.  Upstream Image / Start / Ramp cells are
    way-agnostic (magic-pink-keyed where the way goes, so the engine
    paints the actual way on top at draw), so anything carrying a
    way material has no business in the bridge silhouette.
    Material-substring rather than mesh-name because JH's bridge
    blends suffix-vary the same logical material across twins
    (`Rail.000/.001/.002/.003`, `Wood`/`Wood.001`, `Ballast`/
    `Ballast.001`) and re-use mesh names like `Cube` for very
    different material content across the straight/end/slope/pillar
    set.  Cycles backend matches the vehicle path's BI substitute;
    bridges don't use the EEVEE PBR scaling factor buildings need."""
    # Per-facing model rotation: keep at 0 across all four cameras.
    # JH's bridge-end and bridge-slope geometry is roughly 4-fold
    # symmetric about Z (a brick abutment plus symmetric deck edges)
    # — verified empirically by rotating the model 180° on the N / E
    # facings and finding those views collapse onto the S / W views
    # (same IoU rows in `--match`, same upstream-cell best matches).
    # Once the model lacks geometric features that distinguish the
    # four cardinal ends, no per-facing rotation can lift the N/E
    # cells above the S/W ceiling: it's the bridge-end abutment as
    # seen from N or E, which IS what JH's blend models.  The
    # remaining IoU gap on N/E (0.66-0.76 vs S/W's 0.81-0.91) is
    # presumably a small asymmetry between upstream's authoring and
    # JH's reconstruction, not recoverable from the JH blend alone.
    facings = [
        Facing(
            label=label,
            camera_location=loc,
            camera_rotation_euler=(radians(60), 0.0, radians(cam_z)),
            sun_rotation_euler=sun_rotation_for_camera(cam_z),
            model_rot_z_deg=0.0,
        )
        for label, cam_z, loc in _UPSTREAM_NORMAL_CARDINAL
    ]
    return Viewpoint(
        name="bridge_square",
        image_width=DEFAULT_W,
        ortho_scale=None,  # use blend's authored 12.0
        sun_energy=_SUN_ENERGY,
        sun_energy_scale=1.0,
        fit_kind="none",
        extrinsic=None,
        facings=facings,
        strip_meshes=("Sphere", "Plane.005", "Plane.007"),
        strip_material_substrings=(
            "Rail", "Chair", "Wood", "Ballast", "Tarmac",
        ),
    )


def fence_square_viewpoint() -> Viewpoint:
    """4-cardinal Viewpoint for `grounds/fence.blend` rendered against
    the upstream square cells (`pak/diff_fence.py`).

    Same camera positions as `building_square_viewpoint` (normal
    alignment), but `sun_energy` is pinned directly: the fence blend
    ships a SPOT lamp rather than a SUN, so `_strip_scene`'s authored-
    SUN extraction has nothing to scale.  2.0 matches the post-scale
    value the building viewpoint resolves to under EEVEE.
    """
    facings = [
        Facing(
            label=label,
            camera_location=loc,
            camera_rotation_euler=(radians(60), 0.0, radians(cam_z)),
            sun_rotation_euler=sun_rotation_for_camera(cam_z),
            model_rot_z_deg=0.0,
        )
        for label, cam_z, loc in _UPSTREAM_NORMAL_CARDINAL
    ]
    return Viewpoint(
        name="fence_square",
        image_width=DEFAULT_W,
        ortho_scale=None,   # use blend's authored 12.0
        sun_energy=2.0,
        sun_energy_scale=1.0,
        fit_kind="none",
        extrinsic=None,
        facings=facings,
        engine="BLENDER_EEVEE",
    )


# === Tree viewpoints ======================================================
#
# Trees are billboard-style single-facing scenery: one camera angle per
# (age, season) cell, no rotation table.  Upstream pak128.Britain renders
# every age × season under a fixed S-cardinal normal-alignment camera at
# the blend's authored ortho_scale (12 for the Britain tree blends); ages
# are rendered by scaling the model uniformly between cells.
#
# Per-age scale factors are sampled from upstream PNG bbox heights —
# `oak-summer-{0,1,2,3}_S.png` measure 30, 40, 61, 80 px tall on a 128 px
# image, giving normalised heights 0.375, 0.5, 0.76, 1.0 vs the full-grown
# tree.  Age 4 is a "dead/dormant" stage upstream maps to `oak-winter-3`
# rather than rendering separately; we mirror that mapping at dat-emit
# time, so the bake doesn't render an age-4 cell at all.
#
# Per-season leaf-colour overrides are deferred to phase 2 — the v1 probe
# renders summer only (the .blend's authored Material.001 diffuse) so
# `seasons=1`; autumn / winter / spring / winter-snow need K-means
# centroid sampling from the upstream PNGs the way the way-grade catalog
# was calibrated (see CLAUDE.md → "Per-way material recolour").

_TREE_AGE_SCALES: tuple[float, ...] = (0.375, 0.5, 0.76, 1.0)


def _tree_facings(
    ages: int, seasons: int,
    camera_location: tuple[float, float, float],
    camera_rotation_euler: tuple[float, float, float],
    sun_rotation_euler: tuple[float, float, float],
    model_rot_z_deg: float = 0.0,
) -> list[Facing]:
    """Build one Facing per (season, age) in season-major order.

    Atlas layout (`cols_per_row=ages`): row = season, col = age — matches
    the dat-side `image[age][season]=./<basename>.<season>.<age>` mapping.
    """
    if ages > len(_TREE_AGE_SCALES):
        raise ValueError(
            f"ages={ages} exceeds the per-age scale table; only {len(_TREE_AGE_SCALES)} entries"
        )
    facings: list[Facing] = []
    for s in range(seasons):
        for a in range(ages):
            facings.append(Facing(
                label=f"A{a}_S{s}",
                camera_location=camera_location,
                camera_rotation_euler=camera_rotation_euler,
                sun_rotation_euler=sun_rotation_euler,
                model_rot_z_deg=model_rot_z_deg,
                model_scale=_TREE_AGE_SCALES[a],
            ))
    return facings


def tree_square_viewpoint(ages: int, seasons: int = 1) -> Viewpoint:
    """Square-dimetric Viewpoint for the tree calibration diff.

    Renders `seasons × ages` cells under upstream's S-cardinal
    normal-alignment camera at the blend's authored ortho_scale (12 for
    Britain trees).  `Plane` is stripped on entry — upstream's rendered
    PNGs don't show the large grey ground reference the .blend ships
    with, so whatever the upstream workflow did to hide it, we mirror
    here by name.  EEVEE engine matches the buildings path's BI
    substitute.
    """
    label, cam_z, loc = _UPSTREAM_NORMAL_CARDINAL[0]  # S
    return Viewpoint(
        name="tree_square",
        image_width=DEFAULT_W,
        ortho_scale=None,  # use blend's authored 12.0
        sun_energy=2.0,
        sun_energy_scale=1.0,
        fit_kind="none",
        extrinsic=None,
        facings=_tree_facings(
            ages, seasons,
            camera_location=loc,
            camera_rotation_euler=(radians(60), 0.0, radians(cam_z)),
            sun_rotation_euler=sun_rotation_for_camera(cam_z),
        ),
        engine="BLENDER_EEVEE",
        strip_meshes=("Sphere", "Plane"),
    )


def tree_hex_viewpoint(ages: int, seasons: int = 1) -> Viewpoint:
    """Hex Viewpoint for trees.  Single facing (trees are billboards;
    no rotation table) replicated across `ages × seasons` cells, each
    scaled per `_TREE_AGE_SCALES`.

    `fit_kind="hex"` converts the blend's authored coords into the
    pakset's intra-tile system at `2R/blend_ortho` per blend unit; the
    Britain tree blends are authored at ortho_scale=12, so a full-grown
    tree (~8 blend units tall) lands ~1.3 intra-tile units tall — about
    half the image height, matching upstream's pixel coverage.
    """
    # Britain tree blends ship a SPOT lamp rather than a SUN, so the
    # authored-sun-energy extraction (`_strip_scene` -> `BlendAuthored`)
    # returns None.  Pin sun_energy directly the way `fence_square_
    # viewpoint` does; 2.0 matches the post-scale value the building
    # viewpoints resolve to under EEVEE.
    return Viewpoint(
        name="tree_hex",
        image_width=DEFAULT_W,
        ortho_scale=2.0 * HEX_TILE_RADIUS,
        sun_energy=2.0,
        sun_energy_scale=1.0,
        fit_kind="hex",
        extrinsic=hex_proj_shear(),
        facings=_tree_facings(
            ages, seasons,
            camera_location=_HEX_CAM_LOC,
            camera_rotation_euler=_HEX_CAM_ROT,
            sun_rotation_euler=_HEX_BUILDING_SUN_ROT,
        ),
        engine="BLENDER_EEVEE",
        strip_meshes=("Sphere", "Plane"),
    )


def building_hex_viewpoint(
    layouts: int, dims_x: int, dims_y: int, heights: int = 1,
) -> Viewpoint:
    """Hex Viewpoint for a multi-tile building of footprint `dims_x × dims_y`
    with `layouts` rotation variants and `heights` vertical-stack
    cells.

    Single-tile (`dims_x == dims_y == 1`): one Facing per
    `(layout, height)` rendered at sprite-sized canvas, no slicing
    needed (legacy 1-cell-per-facing path).

    Multi-tile: one Facing per `(layout, height)` rendered at a wider
    canvas sized to cover the full footprint at the hex screen lattice,
    with the model untranslated (artist's authored XYZ contract — the
    blend's per-tile anchor placement passes straight through to
    pixels).  Each Facing carries a `slices` list naming the per-cell
    sprite to crop from the rendered canvas; slice centres land at
    `hex_screen_offset(qx=x, ry=y)` so the engine's paint position for
    that tile and our sliced sprite agree.  Slice labels follow the
    `pak.dat.iter_building_cells` order — even layouts iterate
    `y ∈ [0, dims_y), x ∈ [0, dims_x)`; odd layouts swap to
    `y ∈ [0, dims_x), x ∈ [0, dims_y)`, mirroring the engine's
    `h = (l & 1) ? size.x : size.y` rule in `building_writer.cc`.

    Per-cell Z stacking (`heights > 1`) shifts the whole model down by
    `-h * HEX_HEIGHT_LEVEL_WORLD_Z` per height-h facing; the engine
    paints level h at one full image-height higher and the model's
    height-h slice falls into the hex camera's visible window.  Untested
    end-to-end on a real multi-height port — the first such asset will
    surface whether slicing needs vertical extension too.

    Layout rotation is `(360/layouts) * l` CCW around Z — each layout
    spaces evenly around the circle.  Authored Britain blends sit with
    façades along world X/Y, so 0° and 180° show one wall flat to the
    hex camera; the four off-axis layouts (60°, 120°, 240°, 300°) show
    the two-walls-visible corner silhouette upstream's dimetric corners
    give.  Whether layout 0 actually shows the building's "front" face
    on the camera-side depends on which side the blend's author placed
    it — for the `1600-detatched-house-2f` blend that's the side with
    the gap in the hedge, so layout 0 lands a flat front on the hex N
    edge.
    """
    step = 360.0 / layouts
    multi_tile = dims_x > 1 or dims_y > 1
    # Canvas size and ortho only matter for the multi-tile slicing path
    # (single-tile renders into the sprite-sized canvas the Viewpoint
    # defaults pick up).  The iteration's dims-aware swap means both
    # (dims_x, dims_y) and (dims_y, dims_x) reach the canvas, so the
    # max-koord corner uses `max(dims) - 1` along both axes.
    if multi_tile:
        cx_max, cy_max = hex_tile_screen_offset(
            max(dims_x, dims_y) - 1, max(dims_x, dims_y) - 1,
        )
        canvas_w = int(math.ceil(cx_max + DEFAULT_W))
        canvas_h = int(math.ceil(cy_max + DEFAULT_W))
        # ortho_scale = canvas width in world units at the standard hex
        # pixel rate (W/(2R) px per world unit).  Larger dimension wins
        # in Blender's camera; pick max(w, h).
        ortho_for_canvas = 2.0 * HEX_TILE_RADIUS * max(canvas_w, canvas_h) / DEFAULT_W
    else:
        cx_max = cy_max = 0.0
        canvas_w = canvas_h = None
        ortho_for_canvas = 2.0 * HEX_TILE_RADIUS

    facings: list[Facing] = []
    # Iteration order `h, l, y, x` mirrors `pak.dat.iter_building_cells`
    # within a single season — each (h) becomes one atlas row, with
    # layouts spanning columns left-to-right (each layout block is a
    # `dims_x*dims_y`-wide footprint).  See `emit_building`'s col
    # formula `l * dims_x*dims_y + y * w + x`.
    for h in range(heights):
        for l in range(layouts):
            if l & 1:
                yh, xw = dims_x, dims_y
            else:
                yh, xw = dims_y, dims_x
            shared_kwargs = dict(
                camera_location=_HEX_CAM_LOC,
                camera_rotation_euler=_HEX_CAM_ROT,
                sun_rotation_euler=_HEX_BUILDING_SUN_ROT,
                model_rot_z_deg=step * l,
                model_translation=(0.0, 0.0, -h * HEX_HEIGHT_LEVEL_WORLD_Z),
            )
            if multi_tile:
                # One Facing per (l, h); slices fan out across the cells
                # at hex screen-koord positions, shifted so the
                # multi-tile footprint sits centred in the canvas.
                slice_list: list[tuple[str, tuple[int, int]]] = []
                for y in range(yh):
                    for x in range(xw):
                        cx_px, cy_px = hex_tile_screen_offset(x, y)
                        slice_list.append((
                            f"L{l}_Y{y}_X{x}_H{h}",
                            (int(round(cx_px - cx_max / 2)),
                             int(round(cy_px - cy_max / 2))),
                        ))
                facings.append(Facing(
                    label=f"L{l}_H{h}", slices=slice_list, **shared_kwargs,
                ))
            else:
                # Single-tile: legacy 1-cell-per-facing — one Facing
                # per cell, square sprite-sized canvas.
                for y in range(yh):
                    for x in range(xw):
                        facings.append(Facing(
                            label=f"L{l}_Y{y}_X{x}_H{h}", **shared_kwargs,
                        ))
    return Viewpoint(
        name="hex_building",
        image_width=DEFAULT_W,
        ortho_scale=ortho_for_canvas,
        sun_energy=None,
        sun_energy_scale=_BI_TO_EEVEE_SUN_SCALE,
        fit_kind="hex",
        extrinsic=hex_proj_shear(),
        facings=facings,
        engine="BLENDER_EEVEE",
        canvas_width=canvas_w,
        canvas_height=canvas_h,
        # Multi-tile blends are authored at `ortho_scale = max(dims) ×
        # per-tile-ortho`; divide so `_compute_fit` reads the per-tile
        # ortho the building actually wants.
        fit_ortho_divisor=float(max(dims_x, dims_y)) if multi_tile else 1.0,
    )
