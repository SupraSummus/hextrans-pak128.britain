"""COM_KG_1870_00_06 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building


# Public house.
SPEC = Building(
    name="COM_KG_1870_00_06",
    type="com",
    copyright="Kieron",
    level=6,
    chance=50,
    intro_year=1870,
    retire_year=1910,
    needs_ground=1,
    population_and_visitor_demand_capacity=96,
    employment_capacity=17,
    mail_demand=10,
    class_proportion=[0, 5, 45, 50, 0],
    class_proportion_jobs=[70, 20, 8, 2, 0],
)
BLEND = "citybuildings/1870-pub.blend"
UPSTREAM_STEM = "citybuildings/images/com/1870-pub.png"


if __name__ == "__main__":
    bake_building_main(SPEC, BLEND, __file__)
