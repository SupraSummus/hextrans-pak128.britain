"""RES_JH_1970_03_04 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='RES_JH_1970_03_04',
    type='res',
    copyright='James',
    level=4,
    chance=15,
    intro_year=1970,
    retire_year=1995,
    needs_ground=1,
    population_and_visitor_demand_capacity=11,
    mail_demand=3,
    class_proportion=[5, 18, 60, 17, 0],
    blend='citybuildings/70-bungalow.blend',
    upstream_dat='citybuildings/res-70.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
