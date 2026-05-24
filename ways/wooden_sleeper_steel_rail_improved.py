"""Improved steel rail on wooden sleepers."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Way

# 95 lb/yard -- the standard weight of rail for many years.
SPEC = Way(
    name='wssri',
    waytype='track',
    intro_year=1888,
    intro_month=11,
    # Late because this was the Underground's standard:
    # http://www.trainweb.org/tubeprune/Surrey%20Quays%20Track.htm
    retire_year=1990,
    retire_month=7,
    topspeed=155,
    max_weight=19,
    wear_capacity=3088800000,
    cost=75000,
    maintenance=500,
    icon_src="./images/wooden_sleeper_steel_rail_improved.3.4",
    cursor_src="./images/wooden_sleeper_steel_rail_improved.3.5",
    blend="ways/ns-cssr.blend",
    upstream_dat="ways/wssri.dat",
    materials={
        "Ballast": (80, 73, 70),
        "Wood": (112, 106, 104),
        "Rail": (137, 131, 126),
        "RailTop": (197, 193, 187),
    },
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
