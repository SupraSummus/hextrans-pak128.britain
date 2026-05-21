"""lswr-t9-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-T9-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1912,
    intro_month=12,
    retire_year=1927,
    retire_month=5,
    speed=145,
    length=5,
    weight=49.6,
    axle_load=18,
    power=318,
    tractive_effort=81,
    payload=0,
    cost=6532500,
    runningcost=137,
    fixed_cost=29444,
    upgrade_price=1306500,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lswr-t9-superheated-malachite-austerity.blend',
    upstream_dat='trains/lswr-t9-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
