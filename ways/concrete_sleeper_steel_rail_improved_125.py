"""Improved steel rail on concrete sleepers (125 mph)."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way

# 113 lb/yard.  Expensive as allows faster running.
SPEC = Way(
    name='cssri-125',
    waytype='track',
    intro_year=1973,
    intro_month=6,
    topspeed=200,
    max_weight=23,
    wear_capacity=4116000000,
    cost=150000,
    maintenance=575,
    blend="ways/ns-cssr.blend",
    materials={
        "Ballast": (106, 106, 106),
        "Wood": (132, 127, 127),
        "Rail": (142, 136, 136),
        "RailTop": (176, 176, 176),
    },
)


if __name__ == "__main__":
    bake_way_main(SPEC, __file__)
