"""lner-em1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-ClassEM1',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='electric',
    intro_year=1940,
    intro_month=8,
    retire_year=1963,
    retire_month=8,
    speed=105,
    length=8,
    weight=88,
    axles=4,
    power=1400,
    gear=80,
    tractive_effort=200,
    payload=0,
    cost=5068000,
    runningcost=281,
    fixed_cost=13519,
    increase_maintenance_after_years=25,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='antman09ful1-class-71.wav',
    constraint_prev=['LNER-ClassEM1', 'none'],
    liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early', 'BR-Revised', 'BR-Blue'],
    way_constraint_permissive=[1],
    blend='trains/Locomotives/lner-em1-lner-green.blend',
    upstream_dat='trains/lner-em1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
