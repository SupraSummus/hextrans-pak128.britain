"""Brick viaduct elevated way (160 km/h, 1000 t)."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Way

SPEC = Way(
    name="BrickViaductElevated",
    waytype="track",
    system_type=1,
    intro_year=1600,
    intro_month=1,
    retire_year=1600,
    retire_month=1,
    topspeed=160,
    max_weight=1000,
    wear_capacity=3088800000,
    cost=4480000,
    maintenance=205,
    blend="ways/brick_viaduct/straight.blend",
    blend_source="jh",
    upstream_dat="ways/brick-viaduct-elevated.dat",
    inherit_camera=True,
    full_cell=True,
    full_cell_rotations={"NS": 90.0},
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
