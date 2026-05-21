"""lswr-l12."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-L12',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1904,
    intro_month=6,
    retire_year=1912,
    retire_month=5,
    speed=143,
    length=5,
    weight=55.1,
    axle_load=16,
    power=303,
    tractive_effort=79,
    payload=0,
    cost=6552500,
    runningcost=131,
    fixed_cost=29460,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green'],
    upgrade=['LSWR-L12-superheated'],
    blend='trains/Locomotives/lswr-l12-superheated-austerity.blend',
    upstream_dat='trains/lswr-l12.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
