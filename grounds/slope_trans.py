#!/usr/bin/env python3
"""Bake the hex pakset's slope-transition deliverable.

Per `(slope, corner_mask)` cell carrying the alpha mask the engine uses
for two related transitions:

  * **Climate-corner mixing** — `grund.cc::display` calls
        draw_alpha(get_climate_tile(higher_climate, slope),
                   get_alpha_tile(slope, climate_corners),
                   ALPHA_GREEN | ALPHA_BLUE, ...)
    on each corner that has a same-height neighbour at a higher climate.

  * **Snowline transition** — both `ALPHA_GREEN | ALPHA_BLUE` (snowline
    sitting on flat ground) and `ALPHA_BLUE` (snowline crossing
    mid-slope, snow only on the highest corners) read the same atlas.

The three-colour band encoding:

  RED   — alpha=0 under both keys.  Base ground stays.
  GREEN — opaque under ALPHA_GREEN | ALPHA_BLUE; transparent under
          ALPHA_BLUE alone.  Shows on case-1 transitions only.
  BLUE  — opaque under both keys (the highest mask region).

Strength across the tile is the centre-fan barycentric mix of corner
mask values with `centre = 0.0` so own-biome wins at the centre — same
land-bias structure as `texture_shore`, looser parameters.

Realisability rule (only emit masks that can appear on real terrain):
every set bit has at least one set cyclic neighbour mod 6.  Climate
transitions are unions of 2-bit edge pairs (a same-height neighbour
sets both endpoints of the shared edge); isolated bits never appear
on the climate path.  Snowline-only masks with isolated bits (e.g.
single-corner-up slopes) resolve to IMG_EMPTY here and lose their snow
overlay — see TODO.md.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from tools.threed import hex_synth


SLOPE_RED   = np.array([255, 0,   0,   255], dtype=np.uint8)
SLOPE_GREEN = np.array([0,   255, 0,   255], dtype=np.uint8)
SLOPE_BLUE  = np.array([0,   0,   255, 255], dtype=np.uint8)


def render_slope(slope: int, corner_mask: int,
                 geom: hex_synth.HexGeom | None = None) -> np.ndarray:
    """Render one `(slope, corner_mask)` slope-transition cell."""
    if geom is None:
        geom = hex_synth.HexGeom()

    silhouette = hex_synth.silhouette_mask(slope, geom)
    weight = [(corner_mask >> i) & 1 for i in range(hex_synth.CORNER_COUNT)]
    strength = hex_synth.centre_fan_field(slope, weight, 0.0, geom)

    xs = np.arange(geom.w, dtype=np.uint32)
    ys = np.arange(geom.h, dtype=np.uint32)
    gx, gy = np.meshgrid(xs, ys)
    jitter = (hex_synth.hash_noise01(gx, gy) - 0.5) * 0.8
    s = strength + jitter

    is_blue  = silhouette & (s >= 0.85)
    is_green = silhouette & (s >= 0.5) & ~is_blue
    is_red   = silhouette & ~is_blue & ~is_green

    buf = np.zeros((geom.h, geom.w, 4), dtype=np.uint8)
    buf[is_red]   = SLOPE_RED
    buf[is_green] = SLOPE_GREEN
    buf[is_blue]  = SLOPE_BLUE
    return buf


def _is_edge_union(mask: int, n: int) -> bool:
    """True iff every set bit has at least one set cyclic neighbour mod n."""
    if mask == 0:
        return False
    for i in range(n):
        if (mask >> i) & 1:
            left  = (mask >> ((i - 1) % n)) & 1
            right = (mask >> ((i + 1) % n)) & 1
            if not (left or right):
                return False
    return True


def _slope_entries(geom):
    """Yield `(slope, corner_mask, render_args, comment)` for every
    realisable slope-trans cell."""
    n = hex_synth.CORNER_COUNT
    for slope in hex_synth.iter_valid_slopes():
        ch = hex_synth.decode_corner_heights(slope)
        for corner_mask in range(1, 1 << n):
            if not _is_edge_union(corner_mask, n):
                continue
            bits = [(corner_mask >> i) & 1 for i in range(n)]
            comment = (
                f"corners=(E={ch[hex_synth.E]} SE={ch[hex_synth.SE]} "
                f"SW={ch[hex_synth.SW]} W={ch[hex_synth.W_C]} "
                f"NW={ch[hex_synth.NW]} NE={ch[hex_synth.NE]}) "
                f"mask=(E={bits[hex_synth.E]} SE={bits[hex_synth.SE]} "
                f"SW={bits[hex_synth.SW]} W={bits[hex_synth.W_C]} "
                f"NW={bits[hex_synth.NW]} NE={bits[hex_synth.NE]})"
            )
            yield slope, corner_mask, (slope, corner_mask), comment


if __name__ == "__main__":
    hex_synth.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name="slope_trans",
        obj_name="SlopeTrans",
        render_cell=lambda slope, corner_mask, geom: render_slope(
            slope, corner_mask, geom=geom),
        iter_entries=_slope_entries,
    )
