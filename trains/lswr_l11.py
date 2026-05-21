"""lswr-l11."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-L11',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1903,
    intro_month=1,
    retire_year=1920,
    retire_month=5,
    speed=116,
    length=5,
    weight=51.4,
    axle_load=17,
    power=298,
    tractive_effort=88,
    payload=0,
    cost=6400000,
    runningcost=129,
    fixed_cost=45333,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lswr-l11-austerity.blend',
    upstream_dat='trains/lswr-l11.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
