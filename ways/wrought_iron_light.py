"""40 lb/yard wrought-iron rail."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


# 40 lb/yard.
SPEC = Way(
    name='wrought_iron_light_track',
    waytype='track',
    intro_year=1834,
    intro_month=6,
    retire_year=1852,
    retire_month=7,
    topspeed=85,
    max_weight=7,
    wear_capacity=142560000,
    cost=32000,
    maintenance=750,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (55, 52, 47),
    "Wood": (85, 80, 64),
    "Rail": (187, 190, 175),
    "RailTop": (226, 229, 226),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
