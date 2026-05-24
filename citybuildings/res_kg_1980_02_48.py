"""RES_KG_1980_02_48 city building."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1980_02_48',
    type='res',
    copyright='Kieron',
    level=48,
    chance=2,
    intro_year=1980,
    needs_ground=1,
    population_and_visitor_demand_capacity=67,
    mail_demand=27,
    class_proportion=[0, 0, 50, 40, 10],
    blend='citybuildings/80-5f-tower-block.blend',
    upstream_dat='citybuildings/res-80.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
