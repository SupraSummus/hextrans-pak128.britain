"""RES_KG_1930_00_02 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1930_00_02',
    type='res',
    copyright='Kieron',
    level=2,
    chance=100,
    intro_year=1930,
    retire_year=1950,
    needs_ground=1,
    population_and_visitor_demand_capacity=12,
    mail_demand=2,
    class_proportion=[0, 0, 75, 25, 0],
    blend='citybuildings/30-detatched-house-2f.blend',
    upstream_dat='citybuildings/res-30.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
