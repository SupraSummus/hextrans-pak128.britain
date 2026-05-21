"""lswr-t14."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-T14',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1911,
    intro_month=5,
    retire_year=1920,
    retire_month=7,
    speed=95,
    length=6,
    weight=77.7,
    axle_load=17,
    power=363,
    tractive_effort=112,
    payload=0,
    cost=9552500,
    runningcost=157,
    fixed_cost=47960,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green'],
    upgrade=['LSWR-T14-superheated'],
    blend='trains/Locomotives/lswr-t14-superheated-austerity.blend',
    upstream_dat='trains/lswr-t14.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
