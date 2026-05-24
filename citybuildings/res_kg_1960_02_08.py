"""RES_KG_1960_02_08 city building."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1960_02_08',
    type='res',
    copyright='Kieron',
    level=4,
    chance=45,
    intro_year=1960,
    retire_year=1980,
    needs_ground=1,
    population_and_visitor_demand_capacity=15,
    mail_demand=5,
    class_proportion=[10, 65, 23, 2, 0],
    blend='citybuildings/60-council-house-b.blend',
    upstream_dat='citybuildings/res-60.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
