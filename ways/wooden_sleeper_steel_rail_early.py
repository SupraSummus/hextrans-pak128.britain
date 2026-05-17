"""Early steel rail on wooden sleepers."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way

# 80 lb/yard.  Original steel rails from the 1870s onwards should
# be 80 lb/yard -- see Ahrons p. 185.
SPEC = Way(
    name='wssr-early',
    waytype='track',
    intro_year=1868,
    intro_month=3,
    retire_year=1886,
    retire_month=12,
    topspeed=135,
    max_weight=16,
    wear_capacity=1548000000,
    cost=52000,
    maintenance=575,
    blend="ways/ns-cssr.blend",
    materials={
        "Ballast": (67, 59, 57),
        "Wood": (98, 89, 83),
        "Rail": (149, 138, 122),
        "RailTop": (255, 255, 255),
    },
)


if __name__ == "__main__":
    bake_way_main(SPEC, __file__)
