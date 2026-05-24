"""Concrete-sleeper / steel-rail (cssr) main-line track."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Way

# 110 lb/yard flat-bottomed rail.
# http://en.wikipedia.org/wiki/Permanent_way_%28history%29#Post-war_developments
SPEC = Way(
    name="cssr",
    waytype="track",
    intro_year=1968,
    intro_month=3,
    topspeed=160,
    max_weight=22,
    wear_capacity=4128000000,
    cost=140000,
    maintenance=375,
    icon_src="./images/concrete_sleeper_steel_rail.3.4",
    cursor_src="./images/concrete_sleeper_steel_rail.3.5",
    blend="ways/ns-cssr.blend",
    upstream_dat="ways/cssr.dat",
    materials={
        "Ballast": (100, 100, 100),
        "Wood": (134, 134, 134),
        "Rail": (192, 192, 192),
        "RailTop": (255, 255, 255),
    },
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
