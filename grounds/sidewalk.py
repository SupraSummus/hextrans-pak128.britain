#!/usr/bin/env python3
"""Bake the hex sidewalk (city-road pavement) deliverable.

One cell per way-buildable hex slope: a flat-top hex silhouette filled
with warm-grey concrete, per-region Lambert shading, `hash_noise01`-
driven gravel grit on top.  The engine composites the cell under the
road sprite when `weg_t::hat_gehweg()` is true; on flat ground it also
serves as the building's footpath sprite via `gebaeude.cc`.

Slopes a way can't cross are filtered out (`slope_is_way`); the engine
never asks for a sidewalk on those tiles.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pak import bake_grounds, hex_synth
from pak.hex_synth import (
    HexGeom,
    fill_polygon,
    hash_noise01,
    iter_region_polygons,
    region_brightness,
    seal_horizontal_edges,
)

# Single source of truth for the city-pavement grey.  Road bakers
# (sidewalk slabs, kerbs) key off the same value so seams between a
# city road and a sidewalk-only neighbour read as one continuous grey.
PAVEMENT_RGB: tuple[int, int, int] = (135, 143, 124)

BASE_RGB = np.array(PAVEMENT_RGB, dtype=np.float32)
NOISE_AMP = np.float32(50.0)


def _shaded_rgb(brightness: int) -> tuple[int, int, int]:
    """Apply Lambert brightness to BASE_RGB and clamp to uint8."""
    shade = brightness / 256.0
    rgb = np.clip(BASE_RGB * shade, 0, 255).astype(np.uint8)
    return tuple(int(c) for c in rgb)


def render_sidewalk(slope: int, geom: HexGeom | None = None) -> np.ndarray:
    """Render one slope's sidewalk cell as HxWx4 RGBA."""
    if geom is None:
        geom = HexGeom()

    buf = np.zeros((geom.h, geom.w, 4), dtype=np.uint8)
    for region, xs, ys in iter_region_polygons(slope, geom):
        rgb = _shaded_rgb(region_brightness(region, slope, geom))
        fill_polygon(buf, xs, ys, rgb)
        seal_horizontal_edges(buf, xs, ys, rgb)

    iy, ix = np.mgrid[0:geom.h, 0:geom.w]
    delta = ((hash_noise01(ix.astype(np.uint32), iy.astype(np.uint32))
              - 0.5) * NOISE_AMP)
    delta = (delta * (buf[..., 3] > 0))[..., None].astype(np.int16)
    buf[..., :3] = np.clip(buf[..., :3].astype(np.int16) + delta,
                           0, 255).astype(np.uint8)
    return buf


if __name__ == "__main__":
    bake_grounds.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name="sidewalk",
        obj_name="Sidewalk",
        render_cell=lambda slope, half, geom: render_sidewalk(slope, geom=geom),
        iter_entries=hex_synth.slope_keyed_entries(
            halves=1, slope_filter=hex_synth.slope_is_way),
    )
