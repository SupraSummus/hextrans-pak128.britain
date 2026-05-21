"""lms-stanier-8f-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-Stanier-8F-Tender',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1935,
    intro_month=3,
    retire_year=1946,
    retire_month=1,
    speed=90,
    length=4,
    weight=53,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=16,
    years_before_maintenance_max_reached=9,
    constraint_prev=['LMS-Stanier-8F'],
    liverytype=['LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lms-stanier-8f-tender-br.blend',
    upstream_dat='trains/lms-stanier-8f-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
