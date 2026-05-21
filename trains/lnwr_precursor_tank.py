"""lnwr-precursor-tank."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-Precursor-tank',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1906,
    intro_month=1,
    retire_year=1909,
    retire_month=12,
    speed=120,
    length=7,
    weight=76,
    axle_load=17,
    power=279,
    tractive_effort=68,
    payload=0,
    cost=3755000,
    runningcost=109,
    fixed_cost=27129,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LNWR-Black', 'LMS-Standard'],
    blend='trains/Locomotives/lnwr-precursor-tank-lms.blend',
    upstream_dat='trains/lnwr-precursor-tank.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
