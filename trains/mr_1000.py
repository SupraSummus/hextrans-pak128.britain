"""mr-1000."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-1000',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1905,
    intro_month=8,
    retire_year=1915,
    retire_month=1,
    speed=145,
    length=6,
    weight=60.9,
    axle_load=20,
    power=387,
    tractive_effort=97,
    way_wear_factor=83738,
    payload=0,
    cost=7654000,
    runningcost=168,
    fixed_cost=46378,
    upgrade_price=1275667,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-1000-Tender'],
    liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
    upgrade=['MR-1000-superheated'],
    blend='trains/Locomotives/mr-1000-tender-br-unlined.blend',
    upstream_dat='trains/mr-1000.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
