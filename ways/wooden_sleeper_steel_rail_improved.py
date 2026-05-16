"""Improved steel rail on wooden sleepers."""

from __future__ import annotations

from pak.bake import bake_way_main
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
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (80, 73, 70),
    "Wood": (112, 106, 104),
    "Rail": (137, 131, 126),
    "RailTop": (197, 193, 187),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
