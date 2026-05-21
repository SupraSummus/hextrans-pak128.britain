"""mr-1000-class-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-1000-superheated',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1913,
    intro_month=4,
    retire_year=1924,
    retire_month=2,
    speed=145,
    length=6,
    weight=62.6,
    axle_load=20,
    power=394,
    tractive_effort=98,
    way_wear_factor=86075,
    payload=0,
    cost=7732500,
    runningcost=170,
    fixed_cost=46444,
    upgrade_price=1546500,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-1000-Tender'],
    liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/mr-1000.blend',
    upstream_dat='trains/mr-1000-class-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
