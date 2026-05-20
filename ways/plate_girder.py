"""Plate-girder rail bridge (1890-1949).

JH `ways/plate_girder/{straight,end,slope,pillar}.blend` map to the
image / start / ramp / pillar pieces respectively.  Only the
variant-2 (steeper / taller) abutment + pillar set has a JH source;
variant 0, snow / season 1 and depth-clipped Back/Front cells are
pak-wide bridge TODOs (see TODO.md -> "Hex bridge cell coverage").
"""
from __future__ import annotations

from pak.bake import bake_bridge_main
from pak.dat import Bridge

SPEC = Bridge(
    name="PlateGirder",
    waytype="track",
    copyright="kieron/James",
    intro_year=1890,
    intro_month=9,
    retire_year=1949,
    retire_month=1,
    topspeed=160,
    max_weight=400,
    max_length=4,
    cost=2760000,
    maintenance=100,
    has_own_way_graphics=0,
    pillar_distance=2,
    pillar_asymmetric=1,
    blend_image="ways/plate_girder/straight.blend",
    blend_start="ways/plate_girder/end.blend",
    blend_ramp="ways/plate_girder/slope.blend",
    blend_pillar="ways/plate_girder/pillar.blend",
    upstream_dat="ways/plate-girder.dat",
)


if __name__ == "__main__":
    bake_bridge_main(SPEC, __file__)
