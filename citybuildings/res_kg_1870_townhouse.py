"""RES_KG_1870_00_06 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

# Middling semi-detached houses.
SPEC = Building(
    name="RES_KG_1870_00_06",
    type="res",
    copyright="Kieron",
    level=6,
    chance=70,
    intro_year=1870,
    retire_year=1890,
    needs_ground=1,
    population_and_visitor_demand_capacity=38,
    class_proportion=[0, 20, 65, 15, 0],
)
BLEND = "citybuildings/1870-townhouse-3f.blend"
UPSTREAM_STEM = "citybuildings/images/res/1870-townhouse-3f.png"


if __name__ == "__main__":
    bake_building_main(SPEC, BLEND, __file__)
