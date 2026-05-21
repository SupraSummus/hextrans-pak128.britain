"""lms-stanier-7p-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Streamlined version only
SPEC = Vehicle(
    name='LMS-Stanier-7P-Tender',
    waytype='track',
    copyright='Kieron',
    freight='None',
    intro_year=1937,
    intro_month=6,
    retire_year=1954,
    retire_month=4,
    speed=160,
    length=4,
    weight=56,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=6,
    years_before_maintenance_max_reached=10,
    constraint_prev=['LMS-Stanier-7P', 'LMS-Stanier-7P-non-streamlined'],
    liverytype=['LMS-Standard', 'LMS-Blue'],
    blend='trains/Locomotives/lms-stanier-7p-tender-blue.blend',
    upstream_dat='trains/lms-stanier-7p-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
