#!/usr/bin/env python3
"""Bake the hex pakset's marker (cursor) deliverable.

Per-slope cell carrying **one half** of the hex outline at the slope's
lifted vertices, drawn as an open polyline:

  * front half: E → SE → SW → W (3 south-side edges)
  * back  half: E → NE → NW → W (3 north-side edges)

The two halves bracket tile content at draw time — back drawn before
vehicles/buildings, front drawn after — so the cursor silhouette wraps
around objects on the tile.  Mirrors `synth_overlay::build_marker`.

Style follows the legacy pak128 cursor: bright orange lines (255,128,0)
on a transparent background.  Two halves per slope (halves=2): k=0 is
front, k=1 is back.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pak import bake_grounds, hex_synth

OUTLINE_COLOR_RGB = (255, 128, 0)


def render_marker(slope: int, background: bool,
                  geom: hex_synth.HexGeom | None = None) -> np.ndarray:
    """Render one slope's marker half.  `background=False` draws the
    front half; `background=True` draws the back half."""
    if geom is None:
        geom = hex_synth.HexGeom()

    path = hex_synth.HEX_BACK_PATH if background else hex_synth.HEX_FRONT_PATH
    buf = np.zeros((geom.h, geom.w, 4), dtype=np.uint8)
    hex_synth.rasterise_outline(buf, geom, slope, path,
                                OUTLINE_COLOR_RGB, closed=False)
    return buf


if __name__ == "__main__":
    bake_grounds.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name="marker",
        obj_name="Marker",
        render_cell=lambda slope, half, geom: render_marker(
            slope, background=(half == 1), geom=geom),
        iter_entries=hex_synth.slope_keyed_entries(halves=2),
    )
