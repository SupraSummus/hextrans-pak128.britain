"""RES_KG_1960_04_03 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1960_04_03',
    type='res',
    copyright='Kieron',
    level=3,
    chance=80,
    intro_year=1960,
    retire_year=1990,
    needs_ground=1,
    population_and_visitor_demand_capacity=8,
    mail_demand=2,
    class_proportion=[10, 65, 23, 2, 0],
    blend='citybuildings/1960-council-house-sm-a.blend',
    upstream_dat='citybuildings/res-60.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
