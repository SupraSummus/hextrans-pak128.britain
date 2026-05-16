"""Cast-iron edge rail (pre-wrought-iron era)."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


# As invented by William Jessop.
# https://en.wikipedia.org/wiki/Wagonway#Metal_rails_introduced
SPEC = Way(
    name='cast_iron_track',
    waytype='track',
    intro_year=1789,
    intro_month=10,
    retire_year=1831,
    retire_month=9,
    topspeed=27,
    max_weight=4,
    wear_capacity=8640000,
    cost=30000,
    maintenance=800,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (63, 55, 44),
    "Wood": (75, 62, 47),
    "Rail": (79, 70, 58),
    "RailTop": (89, 82, 72),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
