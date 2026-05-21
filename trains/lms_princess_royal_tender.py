"""lms-princess-royal-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-Princess-Royal-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    intro_year=1933,
    intro_month=6,
    retire_year=1954,
    retire_month=4,
    speed=160,
    length=4,
    weight=55,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=7,
    years_before_maintenance_max_reached=10,
    constraint_prev=['LMS-Princess-Royal', 'LMS-Stanier-7P-non-streamlined'],
    liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lms-princess-royal-tender-wartime.blend',
    upstream_dat='trains/lms-princess-royal-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
