#!/usr/bin/env python3
"""Bake the hex pakset's climate-boundary fence deliverable.

`ground_desc_t::fences` is the back-edge fence overlay drawn at
climate / elevation transitions where a back-wall slot would
otherwise expose hidden ground.  Engine indexes by a 3-bit
wall-presence mask `fence_offset = fence[0] + 2*fence[1] + 4*fence[2]`
(see `grund_t::calc_back_image`), then `typ = fence_offset - 1 +
(artificial ? FENCE_IMAGE_COUNT : 0)` with `FENCE_IMAGE_COUNT = 3`,
so the pakset ships at minimum 6 sprites covering the 3 legacy
single-wall + pair combos × {natural, artificial}.

The 3 hex back-walls match the engine's `back_wall_geometry[]` table
(`grund/grund.cc`): wall 0 = NW edge (W↔NW corners), wall 1 = N
edge (NW↔NE), wall 2 = NE edge (NE↔E).  Cases involving wall 2 fall
outside this 6-sprite window and render as IMG_EMPTY in-engine —
known gap (see `TODO.md`), engine fix bumps `FENCE_IMAGE_COUNT`.

Style is post-and-rail in the upstream-Britain mould (see
`fence-3.png` etc.): vertical posts every few pixels along each
back-edge plus two horizontal rails connecting their tops and
mid-heights.  Drawn on the flat slope; the engine applies its own
y offset (`display_boden`'s fence branch reads
`corner_nw(get_grund_hang())`).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pak import hex_synth

# Dark-wood brown for posts and rails.  Single palette across all
# three back-walls — upstream Britain ships two-tone (left fence-3
# grey-wood, right fence-4 whitewash) but extending that to three
# hex back-edges with no upstream reference is artistic, not
# port-faithful.  Revisit if in-game the uniform palette reads
# wrong (TODO.md).
FENCE_COLOR_RGB = (74, 50, 30)

# Per-edge fence geometry.  Posts sit at integer step-fractions along
# the edge; each post is a vertical line POST_HEIGHT pixels tall.
# Two rails connect consecutive posts at their tops and roughly
# mid-heights.  Numbers picked to match upstream's ~3-px post spacing
# in a 64-px edge (here ~3 px in a ~32-45 px hex back-edge).
POST_COUNT = 12
POST_HEIGHT = 8
RAIL_OFFSETS = (1, 5)   # y-offset from edge to each rail (top to bottom)

# Which `hex_synth.CLIFF_WALL_ENDPOINTS` slots each typ draws.
_WALL_MASKS: dict[int, tuple[int, ...]] = {
    0: (0,),       # wall 0 only (natural)
    1: (1,),       # wall 1 only
    2: (0, 1),     # walls 0 + 1
    3: (0,),       # wall 0 only (artificial)
    4: (1,),       # wall 1 only
    5: (0, 1),     # walls 0 + 1
}


def _post_anchors(geom: hex_synth.HexGeom, wall: int) -> list[tuple[int, int]]:
    """Integer (x, y) anchors evenly spaced along wall's edge, posts pointing
    up (toward smaller y in screen space)."""
    a, b = hex_synth.CLIFF_WALL_ENDPOINTS[wall]
    ax, ay = geom.vx[a], geom.vy_base[a]
    bx, by = geom.vx[b], geom.vy_base[b]
    pts = []
    for i in range(POST_COUNT + 1):
        t = i / POST_COUNT
        x = int(round(ax + (bx - ax) * t))
        y = int(round(ay + (by - ay) * t))
        pts.append((x, y))
    return pts


def _draw_wall(buf: np.ndarray, geom: hex_synth.HexGeom, wall: int) -> None:
    """Render one back-edge as posts + two parallel rails."""
    anchors = _post_anchors(geom, wall)
    for x, y in anchors:
        hex_synth.draw_line(buf, x, y, x, y - POST_HEIGHT, FENCE_COLOR_RGB)
    for r in RAIL_OFFSETS:
        for (x0, y0), (x1, y1) in zip(anchors, anchors[1:]):
            hex_synth.draw_line(buf, x0, y0 - r, x1, y1 - r, FENCE_COLOR_RGB)


def render_fence(typ: int, geom: hex_synth.HexGeom | None = None) -> np.ndarray:
    """Render one fence-presence-mask cell."""
    if geom is None:
        geom = hex_synth.HexGeom()
    buf = np.zeros((geom.h, geom.w, 4), dtype=np.uint8)
    for wall in _WALL_MASKS[typ]:
        _draw_wall(buf, geom, wall)
    return buf


_TYP_LABEL = {
    0: "wall0 natural",
    1: "wall1 natural",
    2: "walls0+1 natural",
    3: "wall0 artificial",
    4: "wall1 artificial",
    5: "walls0+1 artificial",
}


def _fence_entries(geom):
    for typ in range(6):
        yield typ, 0, (typ,), _TYP_LABEL[typ]


if __name__ == "__main__":
    hex_synth.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name="fence",
        obj_name="Fence",
        render_cell=lambda typ, geom: render_fence(typ, geom=geom),
        iter_entries=_fence_entries,
        default_cols=6,
    )
