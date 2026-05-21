"""lnwr-mansion-house-tank."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-Mansion-House-tank',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1880,
    intro_month=5,
    retire_year=1898,
    retire_month=4,
    speed=86,
    length=5,
    weight=46,
    axle_load=14,
    power=172,
    tractive_effort=57,
    payload=0,
    cost=4680000,
    runningcost=99,
    fixed_cost=27900,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LNWR-Black', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lnwr-mansion-house-tank-lms.blend',
    upstream_dat='trains/lnwr-mansion-house-tank.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
