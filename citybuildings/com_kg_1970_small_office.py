"""COM_KG_1970_00_08 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building


# Two-storey office block.
SPEC = Building(
    name="COM_KG_1970_00_08",
    type="com",
    copyright="Kieron",
    level=8,
    chance=70,
    intro_year=1970,
    retire_year=1990,
    needs_ground=1,
    population_and_visitor_demand_capacity=5,
    employment_capacity=38,
    mail_demand=3,
    class_proportion=[0, 1, 69, 25, 5],
    class_proportion_jobs=[2, 8, 80, 8, 2],
)
BLEND = "citybuildings/70-small-office.blend"
UPSTREAM_STEM = "citybuildings/images/com/70-small-office.png"


if __name__ == "__main__":
    bake_building_main(SPEC, BLEND, __file__)
