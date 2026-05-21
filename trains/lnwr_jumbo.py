"""lnwr-jumbo."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-Jumbo',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1887,
    intro_month=9,
    retire_year=1901,
    retire_month=7,
    speed=145,
    length=5,
    weight=42,
    axle_load=12,
    power=233,
    tractive_effort=49,
    payload=0,
    cost=10038000,
    runningcost=157,
    fixed_cost=32365,
    upgrade_price=1056500,
    increase_maintenance_after_years=35,
    years_before_maintenance_max_reached=25,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-Jumbo-Tender'],
    liverytype=['LNWR-Black', 'LMS-Standard'],
    blend='trains/Locomotives/lnwr-jumbo-tender-lms-black.blend',
    upstream_dat='trains/lnwr-jumbo.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
