"""lms-stanier-5mt-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-Stanier-5MT-Tender',
    waytype='track',
    copyright='Kieron',
    freight='None',
    intro_year=1934,
    intro_month=5,
    retire_year=1951,
    retire_month=4,
    speed=135,
    length=4,
    weight=53,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=10,
    years_before_maintenance_max_reached=13,
    constraint_prev=['LMS-Stanier-5MT'],
    liverytype=['LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lms-stanier-5mt-tender-br.blend',
    upstream_dat='trains/lms-stanier-5mt-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
