"""Pre-MacAdam packed-dirt road."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Way

SPEC = Way(
    name="old_dirt_road",
    waytype="road",
    intro_year=1000,
    intro_month=1,
    retire_year=1898,
    retire_month=4,
    topspeed=9,
    max_weight=1,
    wear_capacity=4000000,
    cost=2000,
    maintenance=16,
    icon_src="./images/dirt-old.3.4",
    cursor_src="./images/dirt-old.3.5",
    blend="ways/dirt_road/standard-city-base.blend",
    upstream_dat="ways/dirt-road.dat",
    materials={
        "Dirt": (92, 71, 55),
    },
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
