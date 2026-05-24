"""RES_KG_1950_01_08 city building."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1950_01_08',
    type='res',
    copyright='Kieron',
    level=8,
    chance=50,
    intro_year=1950,
    retire_year=1970,
    needs_ground=1,
    population_and_visitor_demand_capacity=21,
    mail_demand=9,
    class_proportion=[32, 65, 3, 0, 0],
    blend='citybuildings/50-maissonette-a.blend',
    upstream_dat='citybuildings/res-50.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
