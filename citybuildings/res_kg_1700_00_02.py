"""RES_KG_1700_00_02 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1700_00_02',
    type='res',
    copyright='Kieron',
    level=2,
    chance=90,
    intro_year=1700,
    retire_year=1870,
    needs_ground=1,
    population_and_visitor_demand_capacity=11,
    class_proportion=[0, 40, 100, 75, 0],
    blend='citybuildings/1700-row-house-2f.blend',
    upstream_dat='citybuildings/res-1700.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
