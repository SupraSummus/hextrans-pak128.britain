#!/usr/bin/env python3
"""Bake the hex pakset's ground lightmap deliverable.

The pakset deliverable splits per-tile geometry from per-climate biome
art: a grayscale lightmap PNG carries the hex silhouette and the
per-region Lambert shading; a sibling `texture-climate` descriptor
carries the biome colours.  At runtime the engine multiplies the two
via `create_textured_tile`, so this baker never touches climate colours.

Per-region shading goes through `hex_synth.find_min_partition` so
multi-region slopes (saddles, wedges) get one Lambert face per coplanar
region rather than a single average shade.  Geometry, slope decoding,
partitioning, and polygon fill all live in `tools/threed/hex_synth.py`
so this baker stays in lockstep with the rest of the parametric ground
family when the engine's synth_geometry constants move.

Climate texture is biome art with no tile geometry baked in; this pak
doesn't ship a Britain-flavoured climate texture yet (see TODO.md).

Run:
    python3 -m grounds.light_texture [--w 128] [--cols 12] [--out-dir <dir>]
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from tools.threed import hex_synth
from tools.threed.hex_synth import (
    HexGeom,
    fill_polygon,
    iter_region_polygons,
    region_brightness,
    seal_horizontal_edges,
)
from tools.threed.lightmap import brightness_to_grey_rgb


def render_lightmap(slope: int, geom: HexGeom | None = None) -> np.ndarray:
    """Render one slope's lightmap cell.

    Per-region Lambert brightness encoded as a 5-bit grey via
    `brightness_to_grey_rgb` — see `tools/threed/lightmap.py` for the
    `create_textured_tile` multiplier convention and the reserved-
    palette dodge.

    Hex shape is carried in the alpha channel (255 inside, 0 outside).
    """
    if geom is None:
        geom = HexGeom()

    buf = np.zeros((geom.h, geom.w, 4), dtype=np.uint8)
    for region, xs, ys in iter_region_polygons(slope, geom):
        face_rgb = brightness_to_grey_rgb(region_brightness(region, slope, geom))
        fill_polygon(buf, xs, ys, face_rgb)
        seal_horizontal_edges(buf, xs, ys, face_rgb)

    return buf


if __name__ == "__main__":
    hex_synth.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name="light_texture",
        obj_name="LightTexture",
        render_cell=lambda slope, half, geom: render_lightmap(slope, geom=geom),
        iter_entries=hex_synth.slope_keyed_entries(halves=1),
    )
