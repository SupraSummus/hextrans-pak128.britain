"""60 lb/yard wrought-iron rail."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


# Ahrons p. 95 suggests 55 lb/yard, but axle loading is too low at
# that figure -- 60 lb/yard fits better.
SPEC = Way(
    name='wrought_iron_track',
    waytype='track',
    intro_year=1845,
    intro_month=5,
    retire_year=1872,
    retire_month=6,
    topspeed=110,
    max_weight=10,
    wear_capacity=276480000,
    cost=40000,
    maintenance=700,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (54, 52, 48),
    "Wood": (74, 78, 68),
    "Rail": (106, 105, 100),
    "RailTop": (191, 198, 187),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
