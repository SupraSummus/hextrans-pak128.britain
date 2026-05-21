"""lms-4f-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-4F-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    intro_year=1911,
    intro_month=6,
    retire_year=1941,
    retire_month=4,
    speed=95,
    length=4,
    weight=35,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=17,
    years_before_maintenance_max_reached=14,
    constraint_prev=['LMS-4F'],
    liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lms-4f-tender.blend',
    upstream_dat='trains/lms-4f-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
