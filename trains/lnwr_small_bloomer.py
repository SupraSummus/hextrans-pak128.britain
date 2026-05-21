"""lnwr-small-bloomer."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-small-bloomer',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1853,
    intro_month=4,
    retire_year=1860,
    retire_month=1,
    speed=100,
    length=4,
    weight=23.4,
    axle_load=10,
    power=127,
    tractive_effort=28,
    brake_force=0,
    rolling_resistance=19,
    payload=0,
    cost=12187875,
    runningcost=205,
    fixed_cost=34157,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-Bloomer-Tender'],
    liverytype=['LNWR-Early', 'LNWR-Black'],
    blend='trains/Locomotives/lnwr-small-bloomer-black.blend',
    upstream_dat='trains/lnwr-small-bloomer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
