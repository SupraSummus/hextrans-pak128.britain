"""Improved steel rail on wooden sleepers, intermediate."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way

# 97 1/2 lb/yard as on the GWR -- for 20 t axle loads.
SPEC = Way(
    name='wssri_intermediate',
    waytype='track',
    intro_year=1891,
    intro_month=8,
    retire_year=1965,
    retire_month=1,
    topspeed=160,
    max_weight=20,
    wear_capacity=3564000000,
    cost=90000,
    maintenance=450,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (88, 80, 78),
    "Wood": (117, 111, 109),
    "Rail": (130, 125, 125),
    "RailTop": (180, 177, 172),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
