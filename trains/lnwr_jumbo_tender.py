"""lnwr-jumbo-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-Jumbo-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1887,
    intro_month=9,
    retire_year=1901,
    retire_month=7,
    speed=145,
    length=3,
    weight=25,
    axles=3,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=35,
    years_before_maintenance_max_reached=25,
    constraint_prev=['LNWR-Jumbo'],
    liverytype=['LNWR-Black', 'LMS-Standard'],
    blend='trains/Locomotives/lnwr-jumbo-tender-lms-black.blend',
    upstream_dat='trains/lnwr-jumbo-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
