"""Improved steel rail on concrete sleepers."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


# 130 lb/yard.  Expensive as allows faster running.
SPEC = Way(
    name='cssri',
    waytype='track',
    intro_year=1986,
    intro_month=5,
    topspeed=225,
    max_weight=26,
    wear_capacity=4200000000,
    cost=175000,
    maintenance=630,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (111, 110, 110),
    "Wood": (142, 136, 136),
    "Rail": (154, 146, 146),
    "RailTop": (194, 194, 194),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
