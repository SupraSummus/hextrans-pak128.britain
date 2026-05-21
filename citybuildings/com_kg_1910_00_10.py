"""COM_KG_1910_00_10 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='COM_KG_1910_00_10',
    type='com',
    copyright='Kieron',
    level=10,
    chance=25,
    intro_year=1909,
    intro_month=11,
    retire_year=1932,
    retire_month=6,
    needs_ground=1,
    population_and_visitor_demand_capacity=15,
    employment_capacity=88,
    mail_demand=24,
    class_proportion=[0, 5, 50, 35, 10],
    class_proportion_jobs=[3, 8, 69, 15, 5],
    blend='citybuildings/1910-offices-3f.blend',
    upstream_dat='citybuildings/com-10.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
