"""COM_KG_1960_00_08 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='COM_KG_1960_00_08',
    type='com',
    copyright='Kieron',
    level=8,
    chance=75,
    intro_year=1960,
    retire_year=1980,
    needs_ground=1,
    population_and_visitor_demand_capacity=8,
    employment_capacity=92,
    mail_demand=7,
    class_proportion=[0, 1, 69, 25, 5],
    class_proportion_jobs=[1, 5, 72, 20, 2],
    blend='citybuildings/60-shop-flats.blend',
    upstream_dat='citybuildings/com-60.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
