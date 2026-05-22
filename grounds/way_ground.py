#!/usr/bin/env python3
"""Bake the hex pakset's per-(axis, slope) way-ground lightmap.

`ground_desc_t::way_ground` replaces the natural-ground tile lookup on
slopes carrying a way along one of the three hex axes (NS, NE_SW,
NW_SE).  Same Lambert-shaded silhouette as `light_texture`, but
indexed `Image[axis][slope]` (axis outer, slope inner) and emitted
only for slopes where the engine actually queries — i.e. slopes a
way can be laid along that specific axis (`axis_h_way(slope, axis)`
returns a chord).  Engine source: `descriptor/ground_desc.cc`
init/run loops and `ground/grund.cc::display_way_ground`.

The cell content is identical to `light_texture` for the same slope;
the engine multiplies by the climate texture in `create_textured_tile`
just like the natural ground does.  Per-axis visual differentiation
(flattening the way's chord band, ballast-edge shading, etc.) is a
future enhancement; the v1 atlas just ensures the engine has a sprite
to draw instead of falling back to natural ground on way-bearing
sloped tiles.

Run:
    python3 -m grounds.way_ground [--w 128] [--cols 12] [--out-dir <dir>]
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pak import bake_grounds
from pak.hex_synth import (
    NE_SW,
    NS,
    NW_SE,
    HexGeom,
    axis_h_way,
    fill_polygon,
    iter_region_polygons,
    region_brightness,
    seal_horizontal_edges,
)
from pak.lightmap import brightness_to_grey_rgb

_AXIS_LABELS = {NS: "NS", NE_SW: "NE_SW", NW_SE: "NW_SE"}


def render_way_ground(slope: int, geom: HexGeom | None = None):
    """Render one slope's way-ground lightmap cell.

    Same per-region Lambert pass as `light_texture.render_lightmap`;
    factored independently because the iteration / dat-key shape
    differs (axis-keyed here, slope-keyed there).
    """
    if geom is None:
        geom = HexGeom()

    buf = np.zeros((geom.h, geom.w, 4), dtype=np.uint8)
    for region, xs, ys in iter_region_polygons(slope, geom):
        face_rgb = brightness_to_grey_rgb(region_brightness(region, slope, geom))
        fill_polygon(buf, xs, ys, face_rgb)
        seal_horizontal_edges(buf, xs, ys, face_rgb)
    return buf


def _axis_slope_entries(geom):
    """Yield `(axis, slope, render_args, comment)` for every (axis, slope)
    cell the engine queries: way-buildable along that axis, non-flat.

    The flat slope is excluded — `resolve_way_ground` short-circuits
    on `sl == slope_t::flat` before reaching `get_way_ground_image`."""
    labels = geom.corner_labels
    for axis in (NS, NE_SW, NW_SE):
        for slope in geom.iter_valid_slopes():
            if slope == 0:
                continue
            if axis_h_way(slope, axis) is None:
                continue
            ch = geom.decode_corner_heights(slope)
            inner = " ".join(f"{labels[i]}={ch[i]}" for i in range(geom.corner_count))
            comment = f"axis={_AXIS_LABELS[axis]} corners=({inner})"
            yield axis, slope, (slope,), comment


if __name__ == "__main__":
    bake_grounds.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name="way_ground",
        obj_name="WayGround",
        render_cell=lambda slope, geom: render_way_ground(slope, geom=geom),
        iter_entries=_axis_slope_entries,
    )
