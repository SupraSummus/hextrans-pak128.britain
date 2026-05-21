"""lswr-d15-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-D15-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1916,
    intro_month=8,
    retire_year=1923,
    retire_month=1,
    speed=147,
    length=5,
    weight=62.5,
    axle_load=20,
    power=383,
    tractive_effort=89,
    payload=0,
    cost=8967500,
    runningcost=213,
    fixed_cost=47473,
    upgrade_price=1750500,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lswr-d15-superheated-austerity.blend',
    upstream_dat='trains/lswr-d15-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
