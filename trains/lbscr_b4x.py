"""lbscr-b4x."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-B4x',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1922,
    intro_month=8,
    retire_year=1930,
    retire_month=1,
    speed=150,
    length=4,
    weight=58,
    axle_load=20,
    power=310,
    tractive_effort=87,
    payload=0,
    cost=5900000,
    runningcost=186,
    fixed_cost=44917,
    upgrade_price=1500000,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LBSCR-B4-tender'],
    liverytype=['LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-b4x-austerity.blend',
    upstream_dat='trains/lbscr-b4x.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
