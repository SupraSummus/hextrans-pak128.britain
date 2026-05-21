"""lswr-d15."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-D15',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1912,
    intro_month=2,
    retire_year=1916,
    retire_month=8,
    speed=147,
    length=5,
    weight=60.7,
    axle_load=19,
    power=343,
    tractive_effort=99,
    payload=0,
    cost=8752500,
    runningcost=148,
    fixed_cost=47294,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green'],
    upgrade=['LSWR-D15-superheated'],
    blend='trains/Locomotives/lswr-d15-superheated-austerity.blend',
    upstream_dat='trains/lswr-d15.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
