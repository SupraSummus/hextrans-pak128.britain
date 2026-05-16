#!/usr/bin/env python3
"""Hex pakset's `Outside` ground deliverable -- flat void cell."""

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
