"""RES_KG_1890_01_05 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1890_01_05',
    type='res',
    copyright='Kieron',
    level=5,
    chance=65,
    intro_year=1890,
    retire_year=1910,
    needs_ground=1,
    population_and_visitor_demand_capacity=26,
    class_proportion=[5, 20, 60, 15, 0],
    blend='citybuildings/1890-townhouse-3f.blend',
    upstream_dat='citybuildings/res-1890.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
