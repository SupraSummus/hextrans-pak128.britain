"""RES_KG_1960_03_12 city building."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building

SPEC = Building(
    name='RES_KG_1960_03_12',
    type='res',
    copyright='Kieron',
    level=12,
    chance=40,
    intro_year=1960,
    retire_year=1980,
    needs_ground=1,
    population_and_visitor_demand_capacity=15,
    mail_demand=9,
    class_proportion=[0, 15, 70, 13, 2],
    blend='citybuildings/60-terrace-3f.blend',
    upstream_dat='citybuildings/res-60.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
