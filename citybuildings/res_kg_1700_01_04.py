"""RES_KG_1700_01_04 city building."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1700_01_04',
    type='res',
    copyright='Kieron',
    level=4,
    chance=70,
    intro_year=1700,
    retire_year=1870,
    needs_ground=1,
    population_and_visitor_demand_capacity=20,
    class_proportion=[0, 55, 100, 25, 0],
    blend='citybuildings/1700-sm-row-house-2f.blend',
    upstream_dat='citybuildings/res-1700.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
