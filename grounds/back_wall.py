#!/usr/bin/env python3
"""Bake the hex pakset's back-wall (cliff-face) deliverables.

Emits two ground descriptors in lockstep, one per palette flavor,
under the legacy pak128 `Slopes` / `Basement` namespace:

  * `slopes.{png,dat}`    - Name=Slopes    (natural cliff faces)
  * `basement.{png,dat}`  - Name=Basement  (man-made fundament platform)

Both share the same `(wall, index)` key space (3 walls x 10 indices
= 30 cells per atlas) and the same geometry; only the palette differs.
Engine consumption:
    `(artificial ? fundament : slopes)->get_image(wall, index)`
in `ground_desc_t::get_back_wall_image` and
`get_back_wall_extension_image`.  Index 0 (= "no cliff") is not emitted;
the engine treats the absent slot as IMG_EMPTY.

Wall mapping (the tile's three north-side hex edges):
  * wall 0 — NW edge (W -> NW corners)
  * wall 1 — N  edge (NW -> NE corners)
  * wall 2 — NE edge (NE -> E  corners)

Polygon geometry and `(h1, h2)` encoding live in
`hex_synth.render_cliff_cell` / `hex_synth.decode_cliff_index`; only
the per-(artificial, wall) palette lives here.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from tools.threed import hex_synth


WALL_COUNT = 3
IMAGE_COUNT = hex_synth.CLIFF_IMAGE_COUNT


# Flat-colour palette, indexed by (artificial, wall).  Wall 0 (NW
# edge) faces screen-up-left, wall 1 (N) faces screen-up, wall 2 (NE)
# faces screen-up-right; per-wall darkening hand-picked to keep
# adjacent walls visually distinct under vertical cliff lighting.
FACE_COLOR = {
    (False, 0): ( 74,  66,  41),  # natural,   wall 0 (darkest)
    (False, 1): ( 90,  74,  49),  # natural,   wall 1
    (False, 2): (107,  90,  57),  # natural,   wall 2 (lightest)
    (True,  0): (123, 123, 123),  # fundament, wall 0
    (True,  1): (140, 140, 140),  # fundament, wall 1
    (True,  2): (165, 165, 165),  # fundament, wall 2
}


def render_back_wall(wall: int, index: int, artificial: bool,
                     geom: hex_synth.HexGeom | None = None) -> np.ndarray:
    """Render one cliff-face cell.  Output HxWx4 RGBA; index 0 (= no
    cliff) is never baked but renders as empty for safety."""
    h1, h2 = hex_synth.decode_cliff_index(index)
    return hex_synth.render_cliff_cell(wall, h1, h2,
                                        FACE_COLOR[(artificial, wall)], geom)


def _wall_index_entries(artificial: bool):
    """`iter_entries` for back-wall: wall-major emission order so each
    atlas row carries one wall."""
    def gen(_geom):
        for wall in range(WALL_COUNT):
            for index in range(1, IMAGE_COUNT):
                h1, h2 = hex_synth.decode_cliff_index(index)
                yield wall, index, (wall, index, artificial), \
                      f"wall={wall} h1={h1} h2={h2}"
    return gen


def _bake_flavor(*, asset_name: str, obj_name: str, artificial: bool) -> None:
    hex_synth.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name=asset_name,
        obj_name=obj_name,
        render_cell=lambda wall, index, art, geom: render_back_wall(
            wall, index, artificial=art, geom=geom),
        iter_entries=_wall_index_entries(artificial),
        default_cols=IMAGE_COUNT - 1,  # one row per wall
    )


if __name__ == "__main__":
    _bake_flavor(asset_name="slopes",   obj_name="Slopes",   artificial=False)
    _bake_flavor(asset_name="basement", obj_name="Basement", artificial=True)
