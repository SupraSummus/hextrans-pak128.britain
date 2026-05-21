"""mr-1873."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-1873',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1890,
    intro_month=4,
    retire_year=1903,
    retire_month=5,
    speed=85,
    length=4,
    weight=40,
    axles=3,
    power=221,
    tractive_effort=73,
    way_wear_factor=63000,
    payload=0,
    cost=7616000,
    runningcost=148,
    fixed_cost=30347,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-483-Tender'],
    liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/mr-1873-lms.blend',
    upstream_dat='trains/mr-1873.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
