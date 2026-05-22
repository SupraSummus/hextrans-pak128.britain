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
    icon_src="./images/cast_iron.3.4",
    cursor_src="./images/cast_iron.3.5",
    blend="ways/ns-cssr.blend",
    upstream_dat="ways/cast_iron.dat",
    materials={
        "Ballast": (62, 54, 42),
        "Wood": (77, 66, 51),
        "Rail": (92, 84, 74),
        "RailTop": (223, 223, 223),
    },
)


if __name__ == "__main__":
    bake_way_main(SPEC, __file__)
