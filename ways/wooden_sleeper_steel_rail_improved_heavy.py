"""Improved steel rail on wooden sleepers, heavy."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


# Necessary for the larger steam locomotives of 21--22 t axle loads.
# 22 t axle loads need at least 110 lb/yard, but set to 109 here to
# distinguish from later flat-bottomed 110 lb/yard rail.
SPEC = Way(
    name='wssri_heavy',
    waytype='track',
    intro_year=1925,
    intro_month=8,
    retire_year=1968,
    retire_month=6,
    topspeed=160,
    max_weight=22,
    wear_capacity=4050000000,
    cost=135000,
    maintenance=650,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (91, 84, 82),
    "Wood": (119, 115, 113),
    "Rail": (132, 129, 129),
    "RailTop": (181, 178, 174),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
