"""lnwr-precursor."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-Precursor',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1904,
    intro_month=3,
    retire_year=1910,
    retire_month=5,
    speed=146,
    length=6,
    weight=60.1,
    axle_load=17,
    power=290,
    tractive_effort=81,
    payload=0,
    cost=7500000,
    runningcost=125,
    fixed_cost=30250,
    years_before_maintenance_max_reached=21,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-PrinceOfWales-Tender'],
    liverytype=['LNWR-Black', 'LMS-Standard'],
    blend='trains/Locomotives/lnwr-precursor-lms.blend',
    upstream_dat='trains/lnwr-precursor.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
