"""RES_KG_1890_00_02 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

# Low density townhouses.
SPEC = Building(
    name="RES_KG_1890_00_02",
    type="res",
    copyright="Kieron",
    level=2,
    chance=45,
    intro_year=1890,
    retire_year=1910,
    needs_ground=1,
    population_and_visitor_demand_capacity=18,
    class_proportion=[0, 40, 5, 55, 0],
)
BLEND = "citybuildings/1890-detatched-house-3f.blend"
UPSTREAM_STEM = "citybuildings/images/res/1890-detatched-house-3f.png"


if __name__ == "__main__":
    bake_building_main(SPEC, BLEND, __file__)
