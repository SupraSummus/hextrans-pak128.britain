"""Concrete-sleeper / steel-rail (cssr) main-line track."""

from __future__ import annotations

from pak.bake import bake_way_main
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
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (87, 87, 87),
    "Wood": (118, 118, 118),
    "Rail": (133, 133, 133),
    "RailTop": (183, 183, 183),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
