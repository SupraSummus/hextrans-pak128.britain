"""lswr-k10."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-K10',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1899,
    intro_month=7,
    retire_year=1905,
    retire_month=8,
    speed=110,
    length=5,
    weight=47.4,
    axle_load=16,
    power=247,
    tractive_effort=88,
    payload=0,
    cost=5432500,
    runningcost=165,
    fixed_cost=28527,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['lswr-6-wheel-tender'],
    liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lswr-k10-austerity.blend',
    upstream_dat='trains/lswr-k10.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
