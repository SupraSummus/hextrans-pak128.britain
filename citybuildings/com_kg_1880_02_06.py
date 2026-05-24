"""COM_KG_1880_02_06 city building."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building

SPEC = Building(
    name='COM_KG_1880_02_06',
    type='com',
    copyright='Kieron',
    level=6,
    chance=20,
    intro_year=1880,
    retire_year=1910,
    needs_ground=1,
    population_and_visitor_demand_capacity=75,
    employment_capacity=15,
    mail_demand=4,
    class_proportion=[15, 20, 22, 23, 30],
    class_proportion_jobs=[15, 30, 50, 5, 0],
    blend='citybuildings/1880-terrace-row-shop-2f.blend',
    upstream_dat='citybuildings/com-1880.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
