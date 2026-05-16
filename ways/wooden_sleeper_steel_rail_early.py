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
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (58, 51, 49),
    "Wood": (86, 78, 74),
    "Rail": (99, 90, 86),
    "RailTop": (144, 135, 124),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
