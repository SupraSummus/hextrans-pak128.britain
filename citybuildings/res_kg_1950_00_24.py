"""RES_KG_1950_00_24 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1950_00_24',
    type='res',
    copyright='Kieron',
    level=24,
    chance=10,
    intro_year=1950,
    retire_year=1970,
    needs_ground=1,
    population_and_visitor_demand_capacity=80,
    mail_demand=26,
    class_proportion=[25, 70, 5, 0, 0],
    blend='citybuildings/50-6f-tower-block.blend',
    upstream_dat='citybuildings/res-50.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
