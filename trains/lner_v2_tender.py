"""lner-v2-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-V2-Tender',
    waytype='track',
    copyright='Kieron',
    freight='None',
    intro_year=1936,
    intro_month=6,
    retire_year=1944,
    retire_month=10,
    speed=147,
    length=4,
    weight=52,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=16,
    years_before_maintenance_max_reached=9,
    constraint_prev=['LNER-V2'],
    liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lner-v2-tender-br-black.blend',
    upstream_dat='trains/lner-v2-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
