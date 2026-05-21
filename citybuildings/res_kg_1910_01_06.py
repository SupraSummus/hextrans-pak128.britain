"""RES_KG_1910_01_06 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1910_01_06',
    type='res',
    copyright='Kieron',
    level=6,
    chance=85,
    intro_year=1910,
    retire_year=1930,
    needs_ground=1,
    population_and_visitor_demand_capacity=25,
    mail_demand=9,
    class_proportion=[0, 15, 25, 45, 15],
    blend='citybuildings/1910-townhouse-3f.blend',
    upstream_dat='citybuildings/res-10.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
