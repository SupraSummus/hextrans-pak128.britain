#!/usr/bin/env python3
"""Bake the hex pakset's `Outside` ground deliverable.

Single flat hex cell rendered by the engine on void / out-of-world
tiles (`ground_desc_t::outside`).  Without it the pakset fails to
load with `ground.Outside.pak was not found`, so the file has to ship
even before the rest of the map ground families are ready.

Lives under `pak1file/128/` mirroring upstream's layout — see
`pak1file/readme.txt`, which records that the loader expected a
standalone `ground.Outside.pak` (whether hextrans still demands the
literal filename or merely the object is undocumented here, but
matching the upstream layout is the safe bet).  The Makefile's
`OUTSIDE` target hands makeobj a directory output rather than a
bundled `.pak` filename, so each object emits as `<obj>.<Name>.pak`
on its own.

Style mirrors the legacy `ls-water-outside-128.png`: a flat deep-water
silhouette with no animation.  Reuses `grounds.water`'s deepest-depth
base colour so the void reads as the same body of water that lines
the map's edge, minus the per-stage glints (Outside is `Image[0][0]`
only — one frame, no animation).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from grounds.water import N_DEPTHS, WATER_BASE_RGB, depth_shade_factor
from pak import hex_synth


def render_outside(geom: hex_synth.HexGeom | None = None) -> np.ndarray:
    if geom is None:
        geom = hex_synth.HexGeom()
    factor = depth_shade_factor(N_DEPTHS - 1)
    base_rgb = tuple(int(round(c * factor)) for c in WATER_BASE_RGB)
    buf = np.zeros((geom.h, geom.w, 4), dtype=np.uint8)
    xs_poly, ys_poly = list(geom.vx), geom.lifted_vy(0)
    hex_synth.fill_polygon(buf, xs_poly, ys_poly, base_rgb)
    hex_synth.seal_horizontal_edges(buf, xs_poly, ys_poly, base_rgb)
    return buf


def _outside_entries(_geom):
    yield 0, 0, (), "flat void cell"


if __name__ == "__main__":
    hex_synth.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name="outside",
        obj_name="Outside",
        render_cell=lambda geom: render_outside(geom=geom),
        iter_entries=_outside_entries,
        default_cols=1,
    )
