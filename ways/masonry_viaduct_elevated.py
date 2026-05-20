"""Masonry viaduct elevated way (80 km/h, 175 t)."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way

SPEC = Way(
    name="MasonryViaductElevated",
    waytype="track",
    system_type=1,
    intro_year=1600,
    intro_month=1,
    retire_year=1600,
    retire_month=1,
    topspeed=80,
    max_weight=175,
    wear_capacity=276480000,
    cost=5120000,
    maintenance=205,
    blend="ways/brick_viaduct/straight.blend",
    blend_source="jh",
    upstream_dat="ways/masonry-viaduct-elevated.dat",
    inherit_camera=True,
    full_cell=True,
    full_cell_rotations={"NS": 90.0},
    materials={
        # Swap red-brown brick for warm sandstone; parapets cooler.
        "Brick": (160, 144, 112),
        "LightPaving": (200, 192, 176),
    },
)


if __name__ == "__main__":
    bake_way_main(SPEC, __file__)
