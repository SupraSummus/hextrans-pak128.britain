"""86 lb/yard steel rail on wooden sleepers."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way

# 86 lb/yard.
SPEC = Way(
    name='wssr',
    waytype='track',
    intro_year=1874,
    intro_month=6,
    retire_year=1895,
    retire_month=3,
    topspeed=145,
    max_weight=17,
    wear_capacity=2323200000,
    cost=55000,
    maintenance=550,
    blend="ways/ns-cssr.blend",
    materials={
        "Ballast": (65, 57, 55),
        "Wood": (94, 88, 86),
        "Rail": (106, 101, 101),
        "RailTop": (155, 151, 146),
    },
)


if __name__ == "__main__":
    bake_way_main(SPEC, __file__)
