"""Wrought-iron rail, intermediate weight."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Way

# 50 lb/yard.
SPEC = Way(
    name='wrought_iron_intermediate_track',
    waytype='track',
    intro_year=1837,
    intro_month=8,
    retire_year=1867,
    retire_month=12,
    topspeed=100,
    max_weight=9,
    wear_capacity=231840000,
    cost=36000,
    maintenance=725,
    blend="ways/ns-cssr.blend",
    materials={
        "Ballast": (49, 46, 44),
        "Wood": (69, 66, 61),
        "Rail": (82, 81, 70),
        "RailTop": (124, 109, 98),
    },
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
