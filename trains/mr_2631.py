"""mr-2631."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-2631',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1901,
    intro_month=12,
    retire_year=1905,
    retire_month=9,
    speed=145,
    length=6,
    weight=60.5,
    axle_load=20,
    power=349,
    tractive_effort=86,
    way_wear_factor=83188,
    payload=0,
    cost=7600000,
    runningcost=151,
    fixed_cost=46333,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-1000-Tender'],
    liverytype=['MR-Standard', 'LMS-Standard'],
    upgrade=['MR-1000-superheated', 'MR-1000'],
    blend='trains/Locomotives/mr-2631-lms.blend',
    upstream_dat='trains/mr-2631.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
