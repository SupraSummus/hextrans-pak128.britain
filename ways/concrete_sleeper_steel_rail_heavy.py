"""Heavy steel rail on concrete sleepers."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Way

# 130 lb/yard.  For heavy wagons and general duties, not high speed.
SPEC = Way(
    name='cssr_heavy',
    waytype='track',
    intro_year=1992,
    intro_month=2,
    topspeed=145,
    max_weight=26,
    wear_capacity=4200000000,
    cost=110000,
    maintenance=300,
    blend="ways/ns-cssr.blend",
    materials={
        "Ballast": (95, 95, 95),
        "Wood": (125, 120, 120),
        "Rail": (137, 130, 130),
        "RailTop": (174, 174, 174),
    },
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
