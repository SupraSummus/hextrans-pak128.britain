"""lswr-s11-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-S11-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1920,
    intro_month=3,
    retire_year=1930,
    retire_month=2,
    speed=130,
    length=5,
    weight=48.2,
    axle_load=16,
    power=342,
    tractive_effort=85,
    payload=0,
    cost=6520000,
    runningcost=187,
    fixed_cost=29433,
    upgrade_price=1304000,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['lswr-watercart-tender'],
    liverytype=['LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lswr-s11-superheated-austerity.blend',
    upstream_dat='trains/lswr-s11-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
