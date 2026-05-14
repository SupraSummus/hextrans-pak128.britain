#!/usr/bin/env python3
"""Bake the hex pakset's shore-transition deliverable.

Per `(slope, water_mask)` cell carrying an **ALPHA_RED-keyed alpha mask**
for water tiles drawn on a beach-bordering hex.  The engine's
`grund.cc::display` calls

    draw_alpha(get_water_tile(slope, stage),
               get_beach_tile(slope, water_corners),
               ALPHA_RED, ...)

so only the **red channel** of this image's pixels is read as alpha
intensity (`(masked & 0x7c00) >> 5` → 0..31).  Two colours: pure red
where water shows fully, pure blue where it's suppressed (climate
ground wins).  A position-deterministic hashed dither at the wet/dry
boundary preserves the gritty, soft-edge look.

`water_mask` is the 6-bit hex-corner mask `grund.cc` builds from
`vertex_corner_height(...) == water_climate` checks: bit `i` set means
hex corner `i` (E=0, SE=1, SW=2, W=3, NW=4, NE=5) is at sea level and
bordered by water climate.  Wetness across the tile is the centre-fan
barycentric mix of corner wetness with `centre = 0.0` — pinning the
centre dry keeps a land bite even when all 6 corners border water.

Realisability rule (only emit cells the engine will request):
each wet corner must sit at h=0 (water tile is flat at sea level) AND
have a wet neighbour mod 6 (a wet edge sets both endpoints, never one
alone).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from tools.threed import hex_synth


# ALPHA_RED-keyed two-colour palette.  Engine reads only the red
# channel as alpha; blue's RGB doesn't matter beyond `R == 0`.
SHORE_RED  = np.array([255, 0,   0,   255], dtype=np.uint8)
SHORE_BLUE = np.array([0,   0,   255, 255], dtype=np.uint8)


def render_shore(slope: int, water_mask: int,
                 geom: hex_synth.HexGeom | None = None) -> np.ndarray:
    """Render one `(slope, water_mask)` shore-transition cell."""
    if geom is None:
        geom = hex_synth.HexGeom()

    silhouette = hex_synth.silhouette_mask(slope, geom)
    wet = [(water_mask >> i) & 1 for i in range(hex_synth.CORNER_COUNT)]
    wetness = hex_synth.centre_fan_field(slope, wet, 0.0, geom)

    xs = np.arange(geom.w, dtype=np.uint32)
    ys = np.arange(geom.h, dtype=np.uint32)
    gx, gy = np.meshgrid(xs, ys)
    # Symmetric ±0.2 dither, threshold 0.65 to bias toward land.
    jitter = (hex_synth.hash_noise01(gx, gy) - 0.5) * 0.4

    is_wet = silhouette & ((wetness + jitter) >= 0.65)
    is_dry = silhouette & ~is_wet

    buf = np.zeros((geom.h, geom.w, 4), dtype=np.uint8)
    buf[is_wet] = SHORE_RED
    buf[is_dry] = SHORE_BLUE
    return buf


def _shore_entries(geom):
    """Yield `(slope, water_mask, render_args, comment)` for every
    realisable shore cell."""
    n = hex_synth.CORNER_COUNT
    for slope in hex_synth.iter_valid_slopes():
        ch = hex_synth.decode_corner_heights(slope)
        for water_mask in range(1, 1 << n):
            wets = [(water_mask >> i) & 1 for i in range(n)]
            if any(w and (ch[i] != 0
                          or not (wets[(i - 1) % n] or wets[(i + 1) % n]))
                   for i, w in enumerate(wets)):
                continue

            comment = (
                f"corners=(E={ch[hex_synth.E]} SE={ch[hex_synth.SE]} "
                f"SW={ch[hex_synth.SW]} W={ch[hex_synth.W_C]} "
                f"NW={ch[hex_synth.NW]} NE={ch[hex_synth.NE]}) "
                f"water=(E={wets[hex_synth.E]} SE={wets[hex_synth.SE]} "
                f"SW={wets[hex_synth.SW]} W={wets[hex_synth.W_C]} "
                f"NW={wets[hex_synth.NW]} NE={wets[hex_synth.NE]})"
            )
            yield slope, water_mask, (slope, water_mask), comment


if __name__ == "__main__":
    hex_synth.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name="shore_trans",
        obj_name="ShoreTrans",
        render_cell=lambda slope, water_mask, geom: render_shore(
            slope, water_mask, geom=geom),
        iter_entries=_shore_entries,
    )
