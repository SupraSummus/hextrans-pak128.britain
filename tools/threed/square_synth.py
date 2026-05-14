"""Square-dimetric `Geom` implementation, paired with `hex_synth.HexGeom`.

Purpose is the **upstream-diff harness** in `diff_grounds.py`: re-running
the parametric ground bakers (`grounds/<asset>.py`) through this geom
emits the same atlas + dat but in the upstream pak128.Britain
square-dimetric layout, so the output can be pixel-diffed against
authored upstream PNGs (`grounds/images/texture-lightmap.png`, etc.).
That diff covers slope decode, region partition, Lambert region
shading, polygon fill, edge sealing and atlas layout in one pass —
basically everything in the generation pipeline except the corner
count itself.

The geom mirrors upstream's slope encoding from `landscape/ground.dat`:
corner ordering `(SW, SE, NE, NW)` with base-3 weights `(1, 3, 9, 27)`,
giving `slope ∈ [0, 81)`.  Screen layout matches upstream's 128×128
cells with the flat lozenge spanning `y = 64..127` (top corner pad
absorbs raised-corner lift, same `top_pad = 4 * lift` convention as
`HexGeom`).  Single-corner correspondence between world tile and
screen apex was reverse-engineered from
`grounds/images/texture-lightmap.png` cells 1.6 / 1.7 / 1.4 / 1.5
(slopes sw1 / se1 / ne1 / nw1):

    world SW corner ↔ screen W apex (left,  mid-height)
    world SE corner ↔ screen S apex (centre, bottom)
    world NE corner ↔ screen E apex (right, mid-height)
    world NW corner ↔ screen N apex (centre, top)

The two-chord partition (`(0, 2)` SW–NE and `(1, 3)` SE–NW) is the
degenerate case of the hex chord set — `find_min_partition` handles it
unchanged.
"""

from __future__ import annotations

from tools.threed.hex_synth import (
    DEFAULT_W, HEIGHT_STEP, hex_height_raster_scale_y,
)


# ---- Square corner indices (matching simutrans-standard `slope4_t`) -------

SW, SE, NE, NW = 0, 1, 2, 3
SQUARE_CORNER_COUNT = 4

# slope_t encoding from upstream landscape/ground.dat:
#   Image[1]  = sw1   →  weight 1   on corner SW
#   Image[3]  = se1   →  weight 3   on corner SE
#   Image[9]  = ne1   →  weight 9   on corner NE
#   Image[27] = nw1   →  weight 27  on corner NW
# Two height steps per corner (base-3), max slope id 80.
SQUARE_CORNER_WEIGHTS = (1, 3, 9, 27)
SQUARE_MAX_CORNER_HEIGHT = 2
SQUARE_SLOPE_COUNT = (SQUARE_MAX_CORNER_HEIGHT + 1) ** SQUARE_CORNER_COUNT  # 81

# World XY per corner (south = +Y in the engine's lambert frame, matching
# `HEX_CORNER_PROJECTED_X/Y`).  Used by the generic partition + Lambert.
SQUARE_CORNER_XY = [
    (-1.0,  1.0),  # SW
    ( 1.0,  1.0),  # SE
    ( 1.0, -1.0),  # NE
    (-1.0, -1.0),  # NW
]

# Integer projection of the corner XY for the partition algorithm's
# coplanar test and projected-area calculation.
SQUARE_CORNER_PROJECTED_X = [-1,  1,  1, -1]
SQUARE_CORNER_PROJECTED_Y = [ 1,  1, -1, -1]

# All chords for the partition algorithm — the two diagonals.  They cross
# each other, so `find_min_partition` will only ever pick one at a time.
SQUARE_ALL_CHORDS = [(SW, NE), (SE, NW)]

# Outline traversal — closed quad around the lozenge silhouette.
SQUARE_FULL_PATH = (SW, SE, NE, NW)


def square_decode_corner_heights(slope: int) -> list[int]:
    return [(slope // w) % (SQUARE_MAX_CORNER_HEIGHT + 1)
            for w in SQUARE_CORNER_WEIGHTS]


def square_slope_is_valid(slope: int) -> bool:
    """Normalised + adjacency-valid square slope encoding.

    Same shape as `hex_synth.slope_is_valid`: require `min(ch) == 0`
    (slopes where every corner is raised collapse to elevation-only
    duplicates of a normalised slope) and adjacent corners to differ
    by at most 2 (the double-height "double slope" cap).  Upstream's
    `landscape/ground.dat` enumerates all 81 raw `Image[N]` entries
    and routes the non-normalised ones at engine load time to the
    matching normalised cell; for the diff harness we just skip the
    duplicates (the upstream `Image[N]` lookup handles the mapping).
    """
    if not (0 <= slope < SQUARE_SLOPE_COUNT):
        return False
    ch = square_decode_corner_heights(slope)
    if min(ch) != 0:
        return False
    n = SQUARE_CORNER_COUNT
    for i in range(n):
        j = (i + 1) % n
        if abs(ch[i] - ch[j]) > 2:
            return False
    return True


def square_iter_valid_slopes():
    for slope in range(SQUARE_SLOPE_COUNT):
        if square_slope_is_valid(slope):
            yield slope


class SquareGeom:
    """Pak128.Britain square-dimetric ground geometry.

    Same `Geom` interface as `HexGeom` — `corner_count`,
    `corner_world_xy`, `corner_projected_xy`, `all_chords`,
    `corner_labels`, `full_path`, plus the slope-decoder /
    iter-valid-slopes / slope-is-valid statics — so the generic
    `find_min_partition`, `iter_region_polygons`, `region_brightness`,
    `silhouette_mask`, `rasterise_outline` and `bake_pakset` helpers
    work without branching on projection.
    """

    corner_count = SQUARE_CORNER_COUNT
    corner_labels = ("SW", "SE", "NE", "NW")
    corner_world_xy = SQUARE_CORNER_XY
    corner_projected_xy = list(zip(SQUARE_CORNER_PROJECTED_X,
                                   SQUARE_CORNER_PROJECTED_Y))
    all_chords = SQUARE_ALL_CHORDS
    full_path = SQUARE_FULL_PATH

    def __init__(self, raster_w: int = DEFAULT_W, height_step: int = HEIGHT_STEP):
        u = raster_w // 4
        self.u = u
        self.w = 4 * u
        self.lift = hex_height_raster_scale_y(height_step, self.w)
        self.top_pad = 4 * self.lift
        self.h = 2 * u + self.top_pad
        self.top_y = self.top_pad
        self.mid_y = self.top_pad + u
        self.bot_y = self.top_pad + 2 * u - 1

        # Screen XY for each corner at z = 0 (the flat lozenge).
        #   world SW corner → screen W apex (left,   mid)
        #   world SE corner → screen S apex (centre, bottom)
        #   world NE corner → screen E apex (right,  mid)
        #   world NW corner → screen N apex (centre, top)
        self.vx = [0] * SQUARE_CORNER_COUNT
        self.vy_base = [0] * SQUARE_CORNER_COUNT
        self.vx[SW] = 0;          self.vy_base[SW] = self.mid_y
        self.vx[SE] = 2 * u;      self.vy_base[SE] = self.bot_y
        self.vx[NE] = self.w - 1; self.vy_base[NE] = self.mid_y
        self.vx[NW] = 2 * u;      self.vy_base[NW] = self.top_y

    def lifted_vy(self, slope: int) -> list[int]:
        ch = square_decode_corner_heights(slope)
        return [self.vy_base[i] - ch[i] * self.lift
                for i in range(SQUARE_CORNER_COUNT)]

    @staticmethod
    def decode_corner_heights(slope: int) -> list[int]:
        return square_decode_corner_heights(slope)

    @staticmethod
    def iter_valid_slopes():
        return square_iter_valid_slopes()

    @staticmethod
    def slope_is_valid(slope: int) -> bool:
        return square_slope_is_valid(slope)
