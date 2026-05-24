"""RES_KG_1910_00_04 city building."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1910_00_04',
    type='res',
    copyright='Kieron',
    level=4,
    chance=80,
    intro_year=1910,
    retire_year=1930,
    needs_ground=1,
    population_and_visitor_demand_capacity=18,
    mail_demand=6,
    class_proportion=[0, 10, 55, 35, 0],
    blend='citybuildings/1910-townhouse-2f.blend',
    upstream_dat='citybuildings/res-10.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
