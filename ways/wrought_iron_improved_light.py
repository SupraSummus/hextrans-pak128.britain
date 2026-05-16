"""Improved wrought-iron rail, lighter section."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


# ~75 lb/yard -- see Ahrons p. 95.
SPEC = Way(
    name='wrought_iron_improved_light_track',
    waytype='track',
    intro_year=1850,
    intro_month=4,
    retire_year=1876,
    retire_month=11,
    topspeed=120,
    max_weight=13,
    wear_capacity=446400000,
    cost=45000,
    maintenance=650,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (38, 30, 28),
    "Wood": (64, 63, 55),
    "Rail": (74, 76, 67),
    "RailTop": (121, 117, 112),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
