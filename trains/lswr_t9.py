"""lswr-t9."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-T9',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1899,
    intro_month=7,
    retire_year=1904,
    retire_month=6,
    speed=143,
    length=5,
    weight=46.9,
    axle_load=17,
    power=295,
    tractive_effort=79,
    payload=0,
    cost=6532500,
    runningcost=199,
    fixed_cost=45444,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green'],
    upgrade=['LSWR-T9-superheated'],
    blend='trains/Locomotives/lswr-t9-superheated-malachite-austerity.blend',
    upstream_dat='trains/lswr-t9.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
