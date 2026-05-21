"""lner-em2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-ClassEM2',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='electric',
    intro_year=1953,
    intro_month=7,
    retire_year=1964,
    retire_month=5,
    speed=150,
    length=10,
    weight=103,
    axles=6,
    power=2060,
    gear=80,
    tractive_effort=200,
    payload=0,
    cost=7296000,
    runningcost=413,
    fixed_cost=15067,
    increase_maintenance_after_years=25,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='antman09ful1-class-71.wav',
    constraint_prev=['none'],
    liverytype=['BR-Early', 'BR-Revised', 'BR-Blue'],
    way_constraint_permissive=[1],
    blend='trains/Locomotives/lner-em2-black.blend',
    upstream_dat='trains/lner-em2.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
