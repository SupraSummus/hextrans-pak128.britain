"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-watford-tank',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1895,
    intro_month=3,
    retire_year=1906,
    retire_month=1,
    speed=96,
    length=5,
    weight=71,
    axle_load=19,
    power=208,
    tractive_effort=73,
    payload=0,
    cost=3700000,
    runningcost=119,
    fixed_cost=27083,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LNWR-Black', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lnwr-watford-tank.blend',
    upstream_dat='trains/lnwr-watford-tank.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
