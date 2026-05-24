"""COM_KG_1880_00_10 city building."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building

SPEC = Building(
    name='COM_KG_1880_00_10',
    type='com',
    copyright='Kieron',
    level=10,
    chance=20,
    intro_year=1880,
    retire_year=1910,
    needs_ground=1,
    population_and_visitor_demand_capacity=95,
    employment_capacity=26,
    mail_demand=7,
    class_proportion=[15, 20, 22, 23, 30],
    class_proportion_jobs=[15, 30, 50, 5, 0],
    blend='citybuildings/1880-terrace-row-shop.blend',
    upstream_dat='citybuildings/com-1880.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
