"""COM_KG_1970_02_14 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='COM_KG_1970_02_14',
    type='com',
    copyright='Kieron & WLindley',
    level=14,
    chance=40,
    intro_year=1970,
    retire_year=1990,
    needs_ground=1,
    population_and_visitor_demand_capacity=7,
    employment_capacity=57,
    mail_demand=5,
    class_proportion=[0, 1, 69, 25, 5],
    class_proportion_jobs=[2, 8, 80, 8, 2],
    blend='citybuildings/70-office.blend',
    upstream_dat='citybuildings/com-70.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
