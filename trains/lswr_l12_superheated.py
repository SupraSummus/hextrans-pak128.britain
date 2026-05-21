"""lswr-l12-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-L12-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1915,
    intro_month=10,
    retire_year=1926,
    retire_month=5,
    speed=145,
    length=5,
    weight=56.1,
    axle_load=16,
    power=342,
    tractive_effort=81,
    payload=0,
    cost=6552500,
    runningcost=142,
    fixed_cost=29460,
    upgrade_price=1310500,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lswr-l12-superheated-austerity.blend',
    upstream_dat='trains/lswr-l12-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
