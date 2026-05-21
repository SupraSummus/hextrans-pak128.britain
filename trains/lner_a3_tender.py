"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-A1-Tender',
    waytype='track',
    copyright='Kieron',
    freight='None',
    intro_year=1922,
    intro_month=4,
    retire_year=1935,
    retire_month=4,
    speed=160,
    length=4,
    weight=57,
    axles=4,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=23,
    years_before_maintenance_max_reached=11,
    constraint_prev=['LNER-A1', 'LNER-A3'],
    liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early', 'BR-Green'],
    blend='trains/Locomotives/lner-a3-tender.blend',
    upstream_dat='trains/lner-a3-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
