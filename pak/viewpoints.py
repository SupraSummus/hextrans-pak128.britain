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
  Viewpoint with one Facing per `(layout, height)` rotation variant.
  Each Facing renders the whole footprint into a canvas sized to the
  hex screen lattice (`hex_tile_screen_offset`) and carries a
  `slices` list naming the per-cell sprite to crop from that canvas;
  per-cell `model_translation` is not used (artist-authored XYZ
  contract).

All three feed the same `render_facings()` pipeline; the only
difference is which `Viewpoint` instance gets passed in.
"""

from __future__ import annotations

import math
from functools import partial
from math import radians

from pak.hex_synth import (
    DEFAULT_W,
    HEX_SHEAR_Z_COEF,
    HEX_TILE_RADIUS,
    UPSTREAM_ORTHO_SCALE,
    hex_proj_shear,
)
from pak.render import EEVEE, BlendAuthored, Facing, Slice, Viewpoint

# === Authored-resolution helpers ==========================================
#
# Each viewpoint declares its camera ortho, sun energy and fit matrix as a
# `Callable[[BlendAuthored], …]` so policy lives at the field rather than
# scattered as "scale by N when authored is None" fields on `Viewpoint`.
# The resolvers are module-level functions composed via `functools.partial`
# so a fully-constructed `Viewpoint` round-trips through pickle (carried
# across the subprocess boundary to `pak.render` by `pak.bake.run_render`).

_IDENTITY_4X4: tuple = (
    (1.0, 0.0, 0.0, 0.0),
    (0.0, 1.0, 0.0, 0.0),
    (0.0, 0.0, 1.0, 0.0),
    (0.0, 0.0, 0.0, 1.0),
)


def _scale_diag(s: float) -> tuple:
    return ((s, 0.0, 0.0, 0.0),
            (0.0, s, 0.0, 0.0),
            (0.0, 0.0, s, 0.0),
            (0.0, 0.0, 0.0, 1.0))


def _identity_matrix(_authored: BlendAuthored) -> tuple:
    """`fit_matrix` for square (blend-coord) renders."""
    return _IDENTITY_4X4


def _const_resolver(v: float, _a: BlendAuthored) -> float:
    return v


def _authored_ortho(a: BlendAuthored) -> float:
    """Read `authored.ortho_scale` -- raise if the blend has no ortho
    camera.  Used by viewpoints that want each blend's own authored
    ortho (typically buildings at 12 vs vehicles at 24)."""
    if a.ortho_scale is None:
        raise SystemExit(
            "Viewpoint expected authored ortho_scale; blend has no ortho camera"
        )
    return a.ortho_scale


def _authored_sun_resolver(scale: float, a: BlendAuthored) -> float:
    if a.sun_energy is None:
        raise SystemExit(
            "Viewpoint expected authored sun_energy; blend has no SUN light"
        )
    return a.sun_energy * scale


def _hex_fit_resolver(divisor: float, a: BlendAuthored) -> tuple:
    ortho = (a.ortho_scale if a.ortho_scale is not None
             else UPSTREAM_ORTHO_SCALE)
    return _scale_diag(2.0 * HEX_TILE_RADIUS / (ortho / divisor))


def _fixed_hex_scale_resolver(s: float, _a: BlendAuthored) -> tuple:
    return _scale_diag(s)


def _sun_energy_lighting_resolver(
    inner, scale: float, a: BlendAuthored,
) -> float:
    if a.sun_energy is not None:
        return a.sun_energy * scale
    return inner(a)


def _pinned(v: float):
    """Constant value -- viewpoint ignores authored."""
    return partial(_const_resolver, v)


def _authored_sun(scale: float = 1.0):
    """Read `authored.sun_energy` and scale -- raise if the blend has
    no SUN light.  Building viewpoints pass `_BI_TO_EEVEE_SUN_SCALE`
    to compensate for upstream's BI-authored 0.028 under EEVEE."""
    return partial(_authored_sun_resolver, scale)


def _hex_fit(divisor: float = 1.0):
    """Standard hex fit: `Diagonal(2R / (authored.ortho or UPSTREAM)
    / divisor)`.  `divisor > 1` is the multi-tile correction --
    blends authored at `ortho = per_tile * dims` shrink by `divisor =
    dims` so each tile lands at the per-tile pixel rate.  Falls back
    to `UPSTREAM_ORTHO_SCALE` (vehicle convention, 24) when the blend
    has no ortho camera; the divisor doesn't apply in that case."""
    return partial(_hex_fit_resolver, divisor)


def _fixed_hex_scale(s: float):
    """`fit_matrix` that returns a constant `Diagonal(s)`, independent
    of the blend's authored ortho.  Used by `building_hex_viewpoint`
    where the SPEC's `blend_units_per_tile` is the authoritative
    scale anchor."""
    return partial(_fixed_hex_scale_resolver, s)


def _lighting_overrides_facings(
    facings: list[Facing], lighting,
) -> list[Facing]:
    """Apply `Lighting.sun_elev_deg` / `Lighting.sun_az_offset_deg` to
    every facing, with the same defaults the old `_apply_lighting` used
    when only one of them was set (`elev=30°`, `az=-90°`).  Returns a
    new list; original facings unchanged."""
    if lighting is None or (
        lighting.sun_elev_deg is None and lighting.sun_az_offset_deg is None
    ):
        return facings
    from dataclasses import replace
    elev = lighting.sun_elev_deg if lighting.sun_elev_deg is not None else 30.0
    az = (lighting.sun_az_offset_deg
          if lighting.sun_az_offset_deg is not None else -90.0)
    return [
        replace(f, sun_rotation_euler=sun_rotation_for_camera(
            math.degrees(f.camera_rotation_euler[2]),
            sun_elev_deg=elev, sun_az_offset_deg=az,
        ))
        for f in facings
    ]


def _wrap_sun_energy_with_lighting(sun_energy, lighting):
    """Wrap the viewpoint's `sun_energy` resolver so that when both
    `Lighting.sun_energy_scale` is set AND the blend has an authored
    sun_energy, the override `authored.sun_energy * scale` replaces the
    Viewpoint's resolved value.  Preserves the `_apply_lighting`
    guard: if either is None the original resolver's result stands."""
    if lighting is None or lighting.sun_energy_scale is None:
        return sun_energy
    return partial(_sun_energy_lighting_resolver,
                   sun_energy, lighting.sun_energy_scale)

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
    camera_ortho=_pinned(UPSTREAM_ORTHO_SCALE),
    sun_energy=_pinned(_SUN_ENERGY),
    fit_matrix=_identity_matrix,
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
    camera_ortho=_pinned(2.0 * HEX_TILE_RADIUS),
    sun_energy=_pinned(_SUN_ENERGY),
    fit_matrix=_hex_fit(),
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


def sq_tile_screen_offset(x: float, y: float) -> tuple[float, float]:
    """Simutrans Standard dimetric tile lattice: koord +x heads SE on
    screen, koord +y heads SW.  Accepts floats so per-layout footprint
    centroid shifts can use the same formula.  Used by
    `building_square_viewpoint` for multi-tile slice centring and by
    `pak.diff_buildings` for upstream-cell stitching — single source of
    truth for the koord→screen mapping either side of the diff."""
    return (64.0 * x - 64.0 * y, 32.0 * x + 32.0 * y)


def sq_tile_pixel_mask(
    my_offset: tuple[int, int],
    other_offsets: list[tuple[int, int]] = (),
    image_width: int = DEFAULT_W,
):
    """Per-cell pixel-ownership mask for the square dimetric lattice.

    A multi-tile asset's full-canvas render carries pixels from every
    tile in one image; naïvely cropping a W² window around each tile's
    screen anchor brings in the neighbouring tiles' content.  Upstream
    pak128.Britain assigns each canvas pixel to the tile whose anchor
    minimises the dimetric L1 distance `|Δx| + 2·|Δy|` (ties broken in
    favour of the closer-to-viewer tile, i.e. larger anchor y).  This
    gives a strict partition — verified zero-pixel overlap when
    upstream cells of stonehenge / mechanical-signalbox-large are
    pasted back at their canvas positions.  Bisector lines are
    diagonals at slope ±2 in the lattice (`sx ± 2·sy = const`),
    producing the diamond-corner cuts seen in upstream per-tile
    sprites.

    Intersected with the cell-shape hexagon (apex at `(W/2, 0)` and
    `(W/2, W)`, ground diamond at the cell's lower half), which is the
    right shape for the back-most tile (no closer neighbours).
    Single-tile assets (`other_offsets=()`) collapse to the bare
    hexagon — same shape upstream uses for one-cell buildings.  The
    `+1` slack in the hex bounds absorbs the diamond-diagonal AA-edge
    ring that strict math would clip.

    `my_offset`: this tile's slice centre offset (`cx_px, cy_px`) from
    the canvas centre, same value passed in `Facing.slices`.
    `other_offsets`: every other tile's slice centre.
    """
    import numpy as np
    half = image_width // 2
    full = image_width
    ys, xs = np.indices((full, full))
    dx_cell = xs - half
    # Cell ground anchor at pixel (W/2, 3W/4); cell coords -> canvas
    # offsets from this tile's anchor.
    anchor_y = 3 * full // 4
    dy_cell = ys - anchor_y
    my_dist = np.abs(dx_cell) + 2 * np.abs(dy_cell)
    keep = np.ones((full, full), dtype=bool)
    mx, my = my_offset
    for ox, oy in other_offsets:
        # Other tile's anchor offset relative to ours.  Both anchors
        # land at slice_centre + (0, +32) in canvas, so the anchor-to-
        # anchor delta equals the slice-centre delta.
        rel_x, rel_y = ox - mx, oy - my
        other_dist = np.abs(dx_cell - rel_x) + 2 * np.abs(dy_cell - rel_y)
        # Closer-to-viewer wins ties: `rel_y > 0` means other is below
        # us in screen, so we LOSE ties when rel_y > 0.
        keep &= (my_dist < other_dist) | (
            (my_dist == other_dist) & (rel_y < 0)
        )
    # Cell-shape hexagon.  Top/bottom diamond cuts at the four corners.
    abs_x = np.abs(dx_cell)
    keep &= (abs_x <= 2 * ys + 1) & (abs_x <= 2 * (full - ys) + 1)
    return keep.astype(np.float32)


def hex_tile_pixel_mask(
    my_offset: tuple[int, int],
    other_offsets: list[tuple[int, int]] = (),
    image_width: int = DEFAULT_W,
):
    """Per-cell pixel-ownership mask for the hex lattice.

    Hex analogue of `sq_tile_pixel_mask`.  The `hex_proj_shear` extrinsic
    compresses world y by `1/√3`, so world Euclidean distance² between
    two screen-px offsets `(Δx, Δy)` equals `(Δx² + 3·Δy²) / (W/2R)²`
    (1 world unit in y carries √3 more pixel weight than 1 world unit
    in x).  Voronoi under this metric partitions screen space exactly
    along the projected hex tile edges -- footprint neighbours adjacent
    in the hex lattice (`HEX_KOORD_*_WORLD`) cut cleanly along their
    shared projected edge with no overlap.

    Intersected with the projected hex cell-shape: regular hex with
    corners at `(±W/2, 0)` and `(±W/4, ∓W/4)` relative to the ground
    anchor at `(W/2, 3W/4)`, which is the right shape for an isolated
    tile (no footprint neighbours).  Clips above the ground anchor at
    `dy = -W/4`, so silhouettes extending above the tile footprint get
    cut by the cell-shape rather than carried into the slice.  The
    `+1` slack absorbs the slope-±1 AA edge ring.

    `my_offset`: this tile's slice centre offset (`cx_px, cy_px`).
    `other_offsets`: every other footprint tile's slice centre.
    """
    import numpy as np
    half = image_width // 2
    quarter = image_width // 4
    full = image_width
    ys, xs = np.indices((full, full))
    dx_cell = xs - half
    anchor_y = 3 * full // 4
    dy_cell = ys - anchor_y
    # World-Euclidean distance² scaled by (W/(2R))² is `dx² + 3·dy²`;
    # equivalent for closest-tile comparison.
    my_dist = dx_cell * dx_cell + 3 * dy_cell * dy_cell
    keep = np.ones((full, full), dtype=bool)
    mx, my = my_offset
    for ox, oy in other_offsets:
        rel_x, rel_y = ox - mx, oy - my
        rdx = dx_cell - rel_x
        rdy = dy_cell - rel_y
        other_dist = rdx * rdx + 3 * rdy * rdy
        # Closer-to-viewer wins ties: `rel_y > 0` means other is below
        # us in screen, so we LOSE ties when rel_y > 0.
        keep &= (my_dist < other_dist) | (
            (my_dist == other_dist) & (rel_y < 0)
        )
    # Projected hex cell-shape clip.  `|dy| ≤ W/4 AND |dx| + |dy| ≤
    # W/2` -- the six edges meet the corners (W/2, 0), (±W/4, ±W/4),
    # (-W/2, 0) at equality on each constraint.
    abs_x = np.abs(dx_cell)
    abs_y = np.abs(dy_cell)
    keep &= (abs_y <= quarter + 1) & (abs_x + abs_y <= half + 1)
    return keep.astype(np.float32)


def _building_slices(
    layout: int, height: int, dims_x: int, dims_y: int,
    screen_offset,
    pixel_mask=None,
) -> list[Slice]:
    """Per-(layout, height) slices for a building viewpoint, iterated
    under the engine's `(l & 1) ? (y, x) : (x, y)` dims swap.

    `pixel_mask` skipped on single-cell footprints because clipping
    against the cell-shape would crop content (towers, gables) that
    upstream's 128² single-tile PNGs keep.
    """
    from pak.dat import building_footprint_centroid
    xc, yc = building_footprint_centroid(dims_x, dims_y, layout)
    yh, xw = (dims_x, dims_y) if layout & 1 else (dims_y, dims_x)
    cells = [(y, x) for y in range(yh) for x in range(xw)]
    offsets = [
        tuple(int(round(v)) for v in screen_offset(x - xc, y - yc))
        for y, x in cells
    ]
    def mask_for(i):
        if pixel_mask is None or len(offsets) <= 1:
            return None
        return pixel_mask(
            offsets[i],
            [o for j, o in enumerate(offsets) if j != i],
        )
    return [
        Slice(
            label=f"L{layout}_Y{y}_X{x}_H{height}",
            offset=offsets[i],
            alpha_mask=mask_for(i),
        )
        for i, (y, x) in enumerate(cells)
    ]


def building_square_viewpoint(
    layouts: int, units_per_tile: float, dims_x: int = 1, dims_y: int = 1,
    heights: int = 1, lighting=None,
) -> Viewpoint:
    """Square-dimetric Viewpoint for the N-tile calibration diff: one
    Facing per layout rendered under upstream's normal-alignment
    cardinal cameras, each carrying `slices` listing per-cell positions
    on the layout canvas.  The render harness emits both the full
    canvas (for the stitched multi-tile diff) and per-cell 128² sprites
    (for the single-tile diff or per-cell multi-tile diff).

    Layout `l` selects one of the four cardinal cameras
    (S, W, N, E in `_UPSTREAM_NORMAL_CARDINAL`) — equivalent to upstream
    rotating the camera around the unrotated model, rather than rotating
    the model under a fixed camera the way `building_hex_viewpoint`
    does.  The two conventions render the same silhouette per layout,
    but only the camera-rotation form matches upstream's actually-
    published per-layout PNGs (which is what the diff measures against).
    Heights > 1 still unsupported.
    """
    if heights != 1:
        raise NotImplementedError(
            "square_building viewpoint is single-height only"
        )
    if layouts > len(_UPSTREAM_NORMAL_CARDINAL):
        raise ValueError(
            f"square_building supports up to {len(_UPSTREAM_NORMAL_CARDINAL)} "
            f"layouts (cardinal cameras); got {layouts}"
        )
    # Per-layout model rotation around world Z.  Cam rotates `step` per
    # L (`_UPSTREAM_NORMAL_CARDINAL` cardinal order); model rotating
    # `2·step·l` makes the cam-relative building advance `+step` per L
    # step instead of `-step` -- matching the player's map-rotation
    # direction so each L shows the building from a distinct cam-relative
    # angle.  For 4 layouts: 0°, 180°, 0°, 180°.  Pinned on the signalbox
    # by the rendered building's face arrangement matching upstream's
    # stitched cells.  See TODO.md -> "Multi-tile calibration diff
    # residual per-layout offset" for the per-L positional drift this
    # leaves and the open question of generalising the formula.
    step = 360.0 / layouts
    facings: list[Facing] = []
    for l in range(layouts):
        _label, cam_z, loc = _UPSTREAM_NORMAL_CARDINAL[l]
        facings.append(Facing(
            label=f"L{l}_H0",
            camera_location=loc,
            camera_rotation_euler=(radians(60), 0.0, radians(cam_z)),
            sun_rotation_euler=sun_rotation_for_camera(cam_z),
            model_rot_z_deg=(2.0 * step * l) % 360.0,
            slices=_building_slices(
                l, 0, dims_x, dims_y, sq_tile_screen_offset,
                pixel_mask=sq_tile_pixel_mask,
            ),
        ))
    max_dims = max(dims_x, dims_y)
    canvas_w = canvas_h = DEFAULT_W * max_dims
    camera_ortho = _pinned(units_per_tile * max_dims)
    sun_energy = _wrap_sun_energy_with_lighting(
        _authored_sun(_BI_TO_EEVEE_SUN_SCALE), lighting,
    )
    return Viewpoint(
        name="square_building",
        image_width=DEFAULT_W,
        camera_ortho=camera_ortho,
        # Authored sun energy (0.028 in Britain blends) scaled by
        # `_BI_TO_EEVEE_SUN_SCALE` to compensate for EEVEE PBR; may
        # be further overridden by `Lighting.sun_energy_scale`.
        sun_energy=sun_energy,
        fit_matrix=_identity_matrix,
        extrinsic=None,
        facings=_lighting_overrides_facings(facings, lighting),
        engine=EEVEE,
        canvas_width=canvas_w,
        canvas_height=canvas_h,
        world_ambient=lighting.world_ambient if lighting else None,
    )


# Model rotation per hex bridge label.  Default model heading is
# south (rot z=0); each label rotates the model so the named edge
# faces the hex camera.  Both image (axis) and start/ramp (dir)
# labels live in this one table so adding a label updates one place.
# Pulled per-piece below via `HEX_BRIDGE_PIECE_LABELS` from
# `pak.dat` -- single source of truth for label set + order.
_HEX_BRIDGE_MODEL_ROT_DEG: dict[str, float] = {
    # Axes: 3 orientations 60deg apart (axial -- which end is near
    # doesn't matter, model symmetry handles the flip).
    "n_s":     0.0,
    "ne_sw":  60.0,
    "nw_se": 120.0,
    # Directions: 6 orientations 60deg apart.
    "n":  180.0,
    "ne": 240.0,
    "se": 300.0,
    "s":    0.0,
    "sw":  60.0,
    "nw": 120.0,
}


def bridge_hex_viewpoint(piece: str) -> Viewpoint:
    """Hex Viewpoint for a JH bridge piece blend (image / start / ramp).

    `piece` selects which label set from `HEX_BRIDGE_PIECE_LABELS` to
    render -- 3 axial for `image`, 6 directional for `start` / `ramp`.
    Per-label model rotation comes from `_HEX_BRIDGE_MODEL_ROT_DEG`;
    the camera, sun and projection match `HEX_VIEWPOINT`.  Per-piece
    JH blends (`ways/<family>/{straight,end,slope}.blend`) drop in
    directly.

    Way material substrings (`Rail` / `Chair` / `Wood` / `Ballast` /
    `Tarmac`) and the JH backdrop planes (`Plane.005` / `Plane.007`)
    are stripped on entry -- same set as the square calibration
    viewpoint.  Depth-clipped Back/Front separation is not yet
    implemented; `pak.bake.bake_bridge` emits Back and Front pointing
    at the same atlas cell (see TODO.md -> "Hex bridge cell coverage").

    EEVEE rasteriser + authored-sun (`sun_energy=None`, the blend's
    own value) scaled by `_BI_TO_EEVEE_SUN_SCALE`, matching the
    buildings path.  Bridges are static structural assets in the
    same calibration regime as buildings (upstream BI authoring,
    PBR substitution under EEVEE), and EEVEE is byte-stable across
    CI runners where Cycles drifts on AVX2 transcendentals / embree
    -- see CLAUDE.md -> "CI" -> "Lint" for the engine-choice
    rationale.
    """
    from pak.dat import HEX_BRIDGE_PIECE_LABELS
    if piece not in HEX_BRIDGE_PIECE_LABELS:
        raise ValueError(
            f"bridge_hex_viewpoint: piece must be one of "
            f"{sorted(HEX_BRIDGE_PIECE_LABELS)}, got {piece!r}"
        )
    return Viewpoint(
        name=f"bridge_hex_{piece}",
        image_width=DEFAULT_W,
        camera_ortho=_pinned(2.0 * HEX_TILE_RADIUS),
        sun_energy=_authored_sun(_BI_TO_EEVEE_SUN_SCALE),
        fit_matrix=_hex_fit(),
        extrinsic=hex_proj_shear(),
        facings=[
            Facing(
                label=label,
                camera_location=_HEX_CAM_LOC,
                camera_rotation_euler=_HEX_CAM_ROT,
                sun_rotation_euler=_HEX_BUILDING_SUN_ROT,
                model_rot_z_deg=_HEX_BRIDGE_MODEL_ROT_DEG[label],
            )
            for label in HEX_BRIDGE_PIECE_LABELS[piece]
        ],
        engine=EEVEE,
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
        camera_ortho=_authored_ortho,  # use blend's authored 12.0
        sun_energy=_pinned(_SUN_ENERGY),
        fit_matrix=_identity_matrix,
        extrinsic=None,
        facings=facings,
        strip_meshes=("Sphere", "Plane.005", "Plane.007"),
        strip_material_substrings=(
            "Rail", "Chair", "Wood", "Ballast", "Tarmac",
        ),
    )


# Per-cardinal model rotation for the calibration viewpoint.  Upstream
# pak128.Britain inherits pak64's **high-edge** tunnel-key convention:
# the key names the edge the mountain rises against, so `FrontImage[S]`
# is "mountain south of the portal, mouth points north out of the tile".
# `tunnel_desc.cc:9-34` documents the engine's opposing low-edge
# convention (key names the edge the mouth opens through, which
# `_HEX_TUNNEL_MODEL_ROT_DEG` uses) and the N↔S, E↔W permutation
# between them.  Calibration adopts upstream's convention so cells
# diff label-to-label; the production hex bake stays low-edge.
#
# Mouth authored along +X in the blend, so Z-rotation = world angle of
# the OPPOSITE direction's midpoint (S → mouth +Y north → 90°, etc.).
_SQUARE_TUNNEL_MODEL_ROT_DEG: dict[str, float] = {
    "S":  90.0,
    "N": 270.0,
    "E": 180.0,
    "W":   0.0,
}


def tunnel_square_viewpoint() -> Viewpoint:
    """4-cardinal Viewpoint for JH tunnel portal blends (e.g.
    `ways/stone-tunnel.blend`).  Calibration-only -- the production
    bake uses `tunnel_hex_viewpoint()` to land on the engine's 6-edge
    schema (`hex_keys::edge_names`).

    Single fixed camera (normal alignment, `_UPSTREAM_NORMAL_CARDINAL
    [0]` = cam_z 45 -- the same dimetric pak128.Britain authored its
    square assets in) plus per-facing `model_rot_z_deg` from
    `_SQUARE_TUNNEL_MODEL_ROT_DEG`.  The rotation table uses the
    **high-edge** convention upstream's tunnel atlas was authored in,
    not the low-edge convention `tunnel_hex_viewpoint` uses for the
    production hex bake; see `_SQUARE_TUNNEL_MODEL_ROT_DEG`'s comment.
    """
    _, cam_z, loc = _UPSTREAM_NORMAL_CARDINAL[0]
    facings = [
        Facing(
            label=label,
            camera_location=loc,
            camera_rotation_euler=(radians(60), 0.0, radians(cam_z)),
            sun_rotation_euler=sun_rotation_for_camera(cam_z),
            model_rot_z_deg=rot,
        )
        for label, rot in _SQUARE_TUNNEL_MODEL_ROT_DEG.items()
    ]
    return Viewpoint(
        name="tunnel_square",
        image_width=DEFAULT_W,
        camera_ortho=_authored_ortho,
        sun_energy=_pinned(_SUN_ENERGY),
        fit_matrix=_identity_matrix,
        extrinsic=None,
        facings=facings,
        strip_meshes=("Sphere", "Plane.005", "Plane.007"),
        strip_material_substrings=(
            "Rail", "Chair", "Wood", "Ballast", "Tarmac",
        ),
    )


# Per-hex-edge model rotation for tunnel portals.  The convention
# (visually confirmed against arrow-annotated probe atlases) is
#
#     frontimage[<edge>] = portal whose mouth faces direction <edge>
#
# i.e. the direction a train would exit the tunnel.  Mouth in the JH
# stone-tunnel blend is authored along +X, so the Z rotation needed
# to aim it at edge `e` is the world angle of `e`'s midpoint:
#
#     theta(n) = 90, theta(ne) = 30, theta(se) = 330,
#     theta(s) = 270, theta(sw) = 210, theta(nw) = 150
#
# This is the mirror of the bridge `start` cycle (which steps +60deg
# CW around the world); the bridge convention rotates the model so
# its abutment OPENS INWARD (toward tile centre) at the named edge,
# 180deg from where the tunnel's mouth points.  Tunnels don't share
# that table by accident -- the geometric meaning is different.
_HEX_TUNNEL_MODEL_ROT_DEG: dict[str, float] = {
    "n":   90.0,
    "ne":  30.0,
    "se": 330.0,
    "s":  270.0,
    "sw": 210.0,
    "nw": 150.0,
}


# Camera-to-tile-centre distance along the view axis.  `_HEX_CAM_LOC =
# (0, -10, 0.5)` looks along +Y; `hex_proj_shear()` preserves Y, so the
# model's tile-centre lands at world Y=0, distance 10 from the camera.
_HEX_TUNNEL_CENTRE_DEPTH: float = 10.0

# (layer label, clip_start, clip_end) — Front renders geometry between
# the camera and the tile-centre plane (occludes train); Back renders
# what's past it (drawn under train).  Front-first so it lands in atlas
# row 0; `emit_tunnel` keys `frontimage[…][0]=…0.<col>` / `backimage[…]
# [0]=…1.<col>` accordingly.
_HEX_TUNNEL_LAYERS: tuple[tuple[str, float | None, float | None], ...] = (
    ("front", None, _HEX_TUNNEL_CENTRE_DEPTH),
    ("back", _HEX_TUNNEL_CENTRE_DEPTH, None),
)


def tunnel_hex_viewpoint() -> Viewpoint:
    """Hex Viewpoint for a JH tunnel portal blend (`ways/stone-tunnel.
    blend` and friends).  Renders 12 facings -- Front + Back per hex
    edge -- via a camera depth clip at the tile-centre Y plane; compose
    lays them into a 2-row 6-col atlas (row 0 = Front, row 1 = Back).

    Engine draw order is Back, then ground (rails), then train, then
    Front, so portal arch / crenellations occlude the train while the
    rear interior renders behind it.  Way materials are stripped -- the
    engine paints rails separately -- so upstream-Back-vs-ours-Back IoU
    is not directly comparable (upstream bakes rails into Back).
    """
    from pak.dat import TUNNEL_FACING_LABELS
    facings = [
        Facing(
            label=f"{edge}_{layer}",
            camera_location=_HEX_CAM_LOC,
            camera_rotation_euler=_HEX_CAM_ROT,
            sun_rotation_euler=_HEX_BUILDING_SUN_ROT,
            model_rot_z_deg=_HEX_TUNNEL_MODEL_ROT_DEG[edge],
            clip_start=clip_start,
            clip_end=clip_end,
        )
        for layer, clip_start, clip_end in _HEX_TUNNEL_LAYERS
        for edge in TUNNEL_FACING_LABELS
    ]
    return Viewpoint(
        name="tunnel_hex",
        image_width=DEFAULT_W,
        camera_ortho=_pinned(2.0 * HEX_TILE_RADIUS),
        sun_energy=_authored_sun(_BI_TO_EEVEE_SUN_SCALE),
        fit_matrix=_hex_fit(),
        extrinsic=hex_proj_shear(),
        facings=facings,
        engine=EEVEE,
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
        camera_ortho=_authored_ortho,  # use blend's authored 12.0
        sun_energy=_pinned(2.0),
        fit_matrix=_identity_matrix,
        extrinsic=None,
        facings=facings,
        engine=EEVEE,
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
    _label, cam_z, loc = _UPSTREAM_NORMAL_CARDINAL[0]  # S
    return Viewpoint(
        name="tree_square",
        image_width=DEFAULT_W,
        camera_ortho=_authored_ortho,  # use blend's authored 12.0
        sun_energy=_pinned(2.0),
        fit_matrix=_identity_matrix,
        extrinsic=None,
        facings=_tree_facings(
            ages, seasons,
            camera_location=loc,
            camera_rotation_euler=(radians(60), 0.0, radians(cam_z)),
            sun_rotation_euler=sun_rotation_for_camera(cam_z),
        ),
        engine=EEVEE,
        strip_meshes=("Sphere", "Plane"),
    )


def tree_hex_viewpoint(ages: int, seasons: int = 1) -> Viewpoint:
    """Hex Viewpoint for trees.  Single facing (trees are billboards;
    no rotation table) replicated across `ages × seasons` cells, each
    scaled per `_TREE_AGE_SCALES`.

    `_hex_fit()` converts the blend's authored coords into the
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
        camera_ortho=_pinned(2.0 * HEX_TILE_RADIUS),
        sun_energy=_pinned(2.0),
        fit_matrix=_hex_fit(),
        extrinsic=hex_proj_shear(),
        facings=_tree_facings(
            ages, seasons,
            camera_location=_HEX_CAM_LOC,
            camera_rotation_euler=_HEX_CAM_ROT,
            sun_rotation_euler=_HEX_BUILDING_SUN_ROT,
        ),
        engine=EEVEE,
        strip_meshes=("Sphere", "Plane"),
    )


def building_hex_viewpoint(
    layouts: int, units_per_tile: float,
    dims_x: int, dims_y: int, heights: int = 1,
    lighting=None,
) -> Viewpoint:
    """Hex Viewpoint for an N-tile building of footprint `dims_x × dims_y`
    with `layouts` rotation variants and `heights` vertical-stack cells.

    One Facing per `(layout, height)` rendered into a canvas sized to
    cover the full footprint at the hex screen lattice, with the model
    untranslated (artist's authored XYZ contract — the blend's per-tile
    anchor placement passes straight through to pixels).  Each Facing
    carries a `slices` list naming the per-cell sprite to crop from the
    rendered canvas; slice centres land at `hex_screen_offset(qx=x,
    ry=y)` so the engine's paint position for that tile and our sliced
    sprite agree.  Slice labels follow the `pak.dat.iter_building_cells`
    order — even layouts iterate `y ∈ [0, dims_y), x ∈ [0, dims_x)`;
    odd layouts swap to `y ∈ [0, dims_x), x ∈ [0, dims_y)`, mirroring
    the engine's `h = (l & 1) ? size.x : size.y` rule in
    `building_writer.cc`.  Single-tile (`dims_x == dims_y == 1`) is the
    degenerate case: canvas collapses to sprite size, one slice per
    facing at offset (0, 0).

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
    max_dims = max(dims_x, dims_y)
    # Canvas sized to cover the full footprint at the hex screen lattice.
    # The iteration's dims-aware swap means both (dims_x, dims_y) and
    # (dims_y, dims_x) reach the canvas, so the max-koord corner uses
    # `max_dims - 1` along both axes.  Collapses to (DEFAULT_W,
    # DEFAULT_W) for 1×1 footprints.
    cx_max, cy_max = hex_tile_screen_offset(max_dims - 1, max_dims - 1)
    canvas_w = int(math.ceil(cx_max + DEFAULT_W))
    canvas_h = int(math.ceil(cy_max + DEFAULT_W))
    # ortho_scale = canvas width in world units at the standard hex
    # pixel rate (W/(2R) px per world unit).  Larger dimension wins in
    # Blender's camera; pick max(w, h).
    ortho_for_canvas = 2.0 * HEX_TILE_RADIUS * max(canvas_w, canvas_h) / DEFAULT_W

    facings: list[Facing] = []
    # Iteration order `h, l, y, x` mirrors `pak.dat.iter_building_cells`
    # within a single season — each (h) becomes one atlas row, with
    # layouts spanning columns left-to-right (each layout block is a
    # `dims_x*dims_y`-wide footprint).  See `emit_building`'s col
    # formula `l * dims_x*dims_y + y * w + x`.
    for h in range(heights):
        for l in range(layouts):
            facings.append(Facing(
                label=f"L{l}_H{h}",
                slices=_building_slices(
                    l, h, dims_x, dims_y, hex_tile_screen_offset,
                    pixel_mask=hex_tile_pixel_mask,
                ),
                camera_location=_HEX_CAM_LOC,
                camera_rotation_euler=_HEX_CAM_ROT,
                sun_rotation_euler=_HEX_BUILDING_SUN_ROT,
                model_rot_z_deg=step * l,
                model_translation=(0.0, 0.0, -h * HEX_HEIGHT_LEVEL_WORLD_Z),
            ))
    # Per-layout world width `units_per_tile * max_dims` maps to
    # `max_dims` engine tiles (= `2R * max_dims` engine world).
    fit_matrix = _fixed_hex_scale(
        2.0 * HEX_TILE_RADIUS / (units_per_tile * max_dims),
    )
    sun_energy = _wrap_sun_energy_with_lighting(
        _authored_sun(_BI_TO_EEVEE_SUN_SCALE), lighting,
    )
    return Viewpoint(
        name="hex_building",
        image_width=DEFAULT_W,
        camera_ortho=_pinned(ortho_for_canvas),
        sun_energy=sun_energy,
        fit_matrix=fit_matrix,
        extrinsic=hex_proj_shear(),
        facings=_lighting_overrides_facings(facings, lighting),
        engine=EEVEE,
        canvas_width=canvas_w,
        canvas_height=canvas_h,
        world_ambient=lighting.world_ambient if lighting else None,
    )
