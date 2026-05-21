"""lnwr-precursor-webb."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-precursor-webb',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1874,
    intro_month=3,
    retire_year=1887,
    retire_month=9,
    speed=112,
    length=5,
    weight=33,
    axle_load=12,
    power=180,
    tractive_effort=53,
    brake_force=0,
    payload=0,
    cost=9021000,
    runningcost=246,
    fixed_cost=31518,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-Precedent-Tender'],
    upgrade=['LNWR-Jumbo'],
    blend='trains/Locomotives/lnwr-precursor-webb.blend',
    upstream_dat='trains/lnwr-precursor-webb.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
