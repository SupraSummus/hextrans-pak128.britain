"""Lightweight steel rail on concrete sleepers."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Way

# 98 lb/yard.
# http://en.wikipedia.org/wiki/Permanent_way_%28history%29#Post-war_developments
SPEC = Way(
    name='cssr_light',
    waytype='track',
    intro_year=1968,
    intro_month=8,
    topspeed=120,
    max_weight=20,
    wear_capacity=2397600000,
    cost=105000,
    maintenance=200,
    blend="ways/ns-cssr.blend",
    materials={
        "Ballast": (61, 61, 61),
        "Wood": (95, 95, 95),
        "Rail": (112, 112, 112),
        "RailTop": (168, 168, 168),
    },
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
