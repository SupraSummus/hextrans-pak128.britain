"""RES_KG_1930_01_01 city building."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1930_01_01',
    type='res',
    copyright='Kieron',
    level=1,
    chance=75,
    intro_year=1930,
    retire_year=1950,
    needs_ground=1,
    population_and_visitor_demand_capacity=12,
    mail_demand=1,
    class_proportion=[0, 5, 80, 15, 0],
    blend='citybuildings/1930-detatched-bungalow.blend',
    upstream_dat='citybuildings/res-30.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
