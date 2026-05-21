"""RES_KG_1880_01_06 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1880_01_06',
    type='res',
    copyright='Kieron',
    level=6,
    chance=100,
    intro_year=1880,
    retire_year=1900,
    needs_ground=1,
    population_and_visitor_demand_capacity=56,
    class_proportion=[50, 50, 0, 0, 0],
    blend='citybuildings/1880-terrace-row-house-2f.blend',
    upstream_dat='citybuildings/res-1880.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
