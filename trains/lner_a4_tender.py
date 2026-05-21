"""lner-a4-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-A4-Tender',
    waytype='track',
    copyright='Kieron',
    freight='None',
    intro_year=1935,
    intro_month=4,
    retire_year=1948,
    retire_month=1,
    speed=160,
    length=4,
    weight=64,
    axles=4,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=12,
    years_before_maintenance_max_reached=12,
    constraint_prev=['LNER-A4'],
    liverytype=['LNER-Silver-Jubilee', 'LNER-Cornoation', 'LNER-Standard', 'WW2-Austerity', 'BR-Early', 'BR-Green'],
    blend='trains/Locomotives/lner-a4-tender-br-green.blend',
    upstream_dat='trains/lner-a4-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
