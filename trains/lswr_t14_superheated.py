"""lswr-t14-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-T14-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1921,
    intro_month=1,
    retire_year=1929,
    retire_month=4,
    speed=100,
    length=6,
    weight=78,
    axle_load=17,
    power=430,
    tractive_effort=98,
    payload=0,
    cost=9552500,
    runningcost=242,
    fixed_cost=47960,
    upgrade_price=1910500,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lswr-t14-superheated-austerity.blend',
    upstream_dat='trains/lswr-t14-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
