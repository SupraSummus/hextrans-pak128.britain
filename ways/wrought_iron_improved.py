"""Improved wrought-iron rail."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Way

# 82 lb/yard.
# http://www.archive.org/stream/steelrailstheir02sellgoog/steelrailstheir02sellgoog_djvu.txt
SPEC = Way(
    name='wrought_iron_improved_track',
    waytype='track',
    intro_year=1855,
    intro_month=3,
    retire_year=1875,
    retire_month=9,
    topspeed=130,
    max_weight=14,
    wear_capacity=576000000,
    cost=46500,
    maintenance=610,
    blend="ways/ns-cssr.blend",
    materials={
        "Ballast": (43, 34, 32),
        "Wood": (72, 70, 62),
        "Rail": (84, 86, 75),
        "RailTop": (136, 131, 126),
    },
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
