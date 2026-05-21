"""lnwr-pow-tank."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-PrinceOfWales-tank',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1910,
    intro_month=4,
    retire_year=1930,
    retire_month=8,
    speed=130,
    length=7,
    weight=78.2,
    axle_load=16,
    power=337,
    tractive_effort=102,
    payload=0,
    cost=9800000,
    runningcost=123,
    fixed_cost=48167,
    increase_maintenance_after_years=20,
    years_before_maintenance_max_reached=20,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LNWR-Black', 'LMS-Standard'],
    blend='trains/Locomotives/lnwr-PoW-tank-lms.blend',
    upstream_dat='trains/lnwr-pow-tank.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
