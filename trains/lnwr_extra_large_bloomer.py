"""lnwr-extra-large-bloomer."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-extra-large-bloomer',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1852,
    intro_month=7,
    retire_year=1864,
    retire_month=2,
    speed=115,
    length=4,
    weight=31.7,
    axle_load=12,
    power=197,
    tractive_effort=35,
    brake_force=0,
    rolling_resistance=19,
    payload=0,
    cost=16670500,
    runningcost=317,
    fixed_cost=37892,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-Bloomer-Tender'],
    liverytype=['LNWR-Early', 'LNWR-Black'],
    blend='trains/Locomotives/lnwr-extra-large-bloomer-black.blend',
    upstream_dat='trains/lnwr-extra-large-bloomer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
