"""lswr-s11."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-S11',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1903,
    intro_month=1,
    retire_year=1915,
    retire_month=4,
    speed=130,
    length=5,
    weight=47.4,
    axle_load=16,
    power=298,
    tractive_effort=85,
    payload=0,
    cost=6520000,
    runningcost=129,
    fixed_cost=45433,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green'],
    upgrade=['LSWR-S11-superheated'],
    blend='trains/Locomotives/lswr-s11-superheated-austerity.blend',
    upstream_dat='trains/lswr-s11.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
