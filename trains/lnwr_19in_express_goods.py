"""lnwr-19in-express-goods."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-19in-express-goods',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1906,
    intro_month=1,
    retire_year=1909,
    retire_month=11,
    speed=100,
    length=6,
    weight=64,
    axle_load=15,
    power=334,
    tractive_effort=109,
    payload=0,
    cost=99000000,
    runningcost=159,
    fixed_cost=122500,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-PrinceOfWales-Tender'],
    liverytype=['LNWR-Black', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lnwr-19in-express-goods-br.blend',
    upstream_dat='trains/lnwr-19in-express-goods.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
