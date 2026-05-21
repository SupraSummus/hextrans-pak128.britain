"""lnwr-PoW."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-PrinceOfWales',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1911,
    intro_month=6,
    retire_year=1924,
    retire_month=1,
    speed=150,
    length=6,
    weight=67.6,
    axle_load=18,
    power=419,
    tractive_effort=97,
    payload=0,
    cost=10000000,
    runningcost=162,
    fixed_cost=48333,
    increase_maintenance_after_years=16,
    years_before_maintenance_max_reached=22,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-PrinceOfWales-Tender'],
    liverytype=['LNWR-Black', 'LMS-Standard'],
    blend='trains/Locomotives/lnwr-PoW-tender-lms-black.blend',
    upstream_dat='trains/lnwr-PoW.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
