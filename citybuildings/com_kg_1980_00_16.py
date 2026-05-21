"""COM_KG_1980_00_16 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building

SPEC = Building(
    name='COM_KG_1980_00_16',
    type='com',
    copyright='Kieron',
    level=16,
    chance=50,
    intro_year=1980,
    needs_ground=1,
    population_and_visitor_demand_capacity=90,
    employment_capacity=66,
    mail_demand=16,
    class_proportion=[17, 18, 21, 22, 22],
    class_proportion_jobs=[5, 16, 37, 27, 15],
    blend='citybuildings/80-shop-offices.blend',
    upstream_dat='citybuildings/com-80.dat',
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
