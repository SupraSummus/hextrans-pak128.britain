"""Minimal hex projection constants for Blender-based bakers.

Vendored subset of `hextrans-pak128/tools/threed/hex_synth.py` and
`render.py` -- only what `hex_render.py` needs. The pak128 file also
carries the procedural rasterizer, slope encoding, cliff cells, etc.;
those don't belong in a Blender harness. Keep this file aligned with
upstream (`SupraSummus/hextrans-pak128`) when constants drift.

Engine source-of-truth: `hextrans/src/simutrans/display/hex_proj.h` and
`display/synth_geometry.h`.
"""

from __future__ import annotations

import math


# Tile raster width (output image pixel width for a single hex cell).
DEFAULT_W = 128

# Per-step logical height; matches `env_t::pak_tile_height_step`.
HEIGHT_STEP = 8

# World-coords corner radius (one entry-edge length).  Bakers express
# asset dimensions in these units so the camera math doesn't depend on W.
HEX_TILE_RADIUS = 1.0

# Pixel lift per world-z unit, shared with pak128 square dimetric so a
# given 3D part has comparable on-screen height in both projections.
PIXELS_PER_UNIT = DEFAULT_W / math.sqrt(2.0)


# Sun: from south (-y), 60 deg above horizon. Light travels north and
# downward.  Used to set a SUN lamp's -Z so shading stays consistent
# across facings (model rotates, sun does not).
SUN_DIR = (
    0.0,
    math.cos(math.radians(60.0)),
    -math.sin(math.radians(60.0)),
)


def hex_proj_shear() -> tuple[tuple[float, ...], ...]:
    """4x4 matrix mapping world (x, y, z) into a render frame in which a
    standard ortho-from-south Blender camera reproduces the hex
    projection.

    Derivation: the engine's projection is
        sx = w/2 + x * (w / (2R))
        sy = base_y - y * (w / (2R sqrt(3))) - z * PIXELS_PER_UNIT
    The y- and z-coefficients on screen-y differ, so a single isotropic
    Blender ortho cannot reproduce it without pre-distortion.  After the
    shear below, a camera with `ortho_scale = 2R` and image width `W`
    looking down +Y sees the right pixels:
        sx_blender = W/2 + x * (W / (2R))                  -> same as engine
        sy_blender = H/2 + (y/sqrt(3) + z*sqrt(2)) * (W/(2R))
                   = H/2 + y * W/(2R sqrt(3)) + z * (W*sqrt(2)/(2R))
                   = H/2 + y * w-coef + z * (W*sqrt(2)/2)
                   z-coef at R=1, W=128: 128*sqrt(2)/2 = 64*sqrt(2) = 90.51
                   PIXELS_PER_UNIT = 128/sqrt(2) = 90.51  -> match
    """
    inv_sqrt3 = 1.0 / math.sqrt(3.0)
    sqrt2 = math.sqrt(2.0)
    # Column-major would matter for some math libs; Blender's `Matrix`
    # constructor takes row-major and we return the same.
    return (
        (1.0, 0.0,       0.0,   0.0),
        (0.0, 1.0,       0.0,   0.0),
        (0.0, inv_sqrt3, sqrt2, 0.0),
        (0.0, 0.0,       0.0,   1.0),
    )
