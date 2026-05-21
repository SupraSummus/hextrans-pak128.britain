"""lbscr-b2x."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-B2x',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1907,
    intro_month=10,
    retire_year=1916,
    retire_month=7,
    speed=132,
    length=5,
    weight=43,
    axle_load=15,
    power=262,
    tractive_effort=67,
    payload=0,
    cost=5900000,
    runningcost=105,
    fixed_cost=28917,
    upgrade_price=2000000,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LBSCR-B2-tender'],
    liverytype=['LBSCR-Marsh', 'SR-Olive-Green'],
    blend='trains/Locomotives/lbscr-b2x-olive.blend',
    upstream_dat='trains/lbscr-b2x.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
