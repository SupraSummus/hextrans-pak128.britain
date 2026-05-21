"""lnwr-mcconnell-large-single."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-mcconnell-large-single',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1861,
    intro_month=7,
    retire_year=1866,
    retire_month=10,
    speed=117,
    length=4,
    weight=34.6,
    axle_load=14,
    power=206,
    tractive_effort=35,
    brake_force=0,
    rolling_resistance=19,
    payload=0,
    cost=17290500,
    runningcost=249,
    fixed_cost=38409,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-Bloomer-Tender'],
    liverytype=['LNWR-Early', 'LNWR-Black'],
    blend='trains/Locomotives/lnwr-mcconnell-large-single-black.blend',
    upstream_dat='trains/lnwr-mcconnell-large-single.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
