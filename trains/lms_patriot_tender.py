"""lms-patriot-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-Patriot-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    intro_year=1930,
    intro_month=11,
    retire_year=1935,
    retire_month=7,
    speed=150,
    length=4,
    weight=43,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=24,
    years_before_maintenance_max_reached=11,
    constraint_prev=['LMS-Patriot'],
    liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lms-patriot-tender-wartime.blend',
    upstream_dat='trains/lms-patriot-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
