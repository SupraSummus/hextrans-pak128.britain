"""RES_KG_1920_00_02 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

# Detached house with sizeable garden.
SPEC = Building(
    name="RES_KG_1920_00_02",
    type="res",
    copyright="Kieron",
    level=2,
    chance=65,
    intro_year=1920,
    retire_year=1940,
    needs_ground=1,
    population_and_visitor_demand_capacity=11,
    mail_demand=4,
    class_proportion=[0, 5, 40, 50, 5],
)
BLEND = "citybuildings/1920-detatched-house-2f.blend"
UPSTREAM_STEM = "citybuildings/images/res/1920-detatched-house-2f.png"


if __name__ == "__main__":
    bake_building_main(SPEC, BLEND, __file__)
