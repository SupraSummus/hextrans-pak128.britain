"""lyr-cl25."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LYR-Class25',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1876,
    intro_month=7,
    retire_year=1895,
    retire_month=4,
    speed=85,
    length=5,
    weight=39,
    axles=3,
    power=215,
    tractive_effort=75,
    way_wear_factor=61425,
    payload=0,
    cost=4051200,
    runningcost=216,
    fixed_cost=27376,
    increase_maintenance_after_years=30,
    years_before_maintenance_max_reached=30,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LYR-Class25-Tender'],
    liverytype=['LYR-Light-Green', 'LYR-Black', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lyr-cl25-light-green.blend',
    upstream_dat='trains/lyr-cl25.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
