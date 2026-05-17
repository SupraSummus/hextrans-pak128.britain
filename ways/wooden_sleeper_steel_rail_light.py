"""Lightweight steel rail on wooden sleepers."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way

# 70 lb/yard branch-line track.
SPEC = Way(
    name='wssr_light',
    waytype='track',
    intro_year=1876,
    intro_month=2,
    retire_year=1903,
    retire_month=4,
    topspeed=80,
    max_weight=15,
    wear_capacity=1008000000,
    cost=32000,
    # Lower than otherwise allowed because of the lower speed limit.
    maintenance=375,
    blend="ways/ns-cssr.blend",
    materials={
        "Ballast": (51, 43, 40),
        "Wood": (78, 67, 61),
        "Rail": (91, 79, 72),
        "RailTop": (140, 130, 116),
    },
)


if __name__ == "__main__":
    bake_way_main(SPEC, __file__)
