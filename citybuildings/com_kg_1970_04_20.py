"""COM_KG_1970_04_20 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='COM_KG_1970_04_20',
    type='com',
    copyright='Kieron & WLindley',
    level=20,
    chance=40,
    intro_year=1970,
    retire_year=1990,
    needs_ground=1,
    population_and_visitor_demand_capacity=12,
    employment_capacity=100,
    mail_demand=8,
    class_proportion=[0, 1, 69, 25, 5],
    class_proportion_jobs=[1, 5, 62, 25, 7],
    blend='citybuildings/70-office.blend',
    upstream_dat='citybuildings/com-70.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
