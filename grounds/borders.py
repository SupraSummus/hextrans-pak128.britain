#!/usr/bin/env python3
"""Bake the hex pakset's grid-border deliverable.

Per-slope cell carrying the **3 north-side edges** of the hex outline
at the slope's lifted vertices — open polyline E → NE → NW → W —
drawn over the tile when `grund_t::show_grid` is on.

Hex equivalent of square pak128's `borders.png` convention: each tile
only draws its top/back edges; the south neighbour's back edges cover
this tile's south side, so the union over all tiles paints every grid
edge exactly once.  Style: thin dark-grey lines on a transparent
background, matching the legacy art.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from tools.threed import hex_synth


OUTLINE_COLOR_RGB = (32, 32, 32)


def render_border(slope: int, geom: hex_synth.HexGeom | None = None) -> np.ndarray:
    """Render one slope's grid-border cell."""
    if geom is None:
        geom = hex_synth.HexGeom()

    buf = np.zeros((geom.h, geom.w, 4), dtype=np.uint8)
    hex_synth.rasterise_outline(buf, geom, slope, hex_synth.HEX_BACK_PATH,
                                OUTLINE_COLOR_RGB, closed=False)
    return buf


if __name__ == "__main__":
    hex_synth.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name="borders",
        obj_name="Borders",
        render_cell=lambda slope, half, geom: render_border(slope, geom=geom),
        iter_entries=hex_synth.slope_keyed_entries(halves=1),
    )
