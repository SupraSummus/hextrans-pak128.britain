"""br-cl52."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class52',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='diesel',
    intro_year=1961,
    intro_month=9,
    retire_year=1964,
    retire_month=1,
    speed=140,
    length=12,
    weight=108,
    axles=6,
    power=2025,
    gear=42,
    tractive_effort=297,
    rolling_resistance=13,
    payload=0,
    cost=12173000,
    runningcost=1014,
    fixed_cost=18453,
    increase_maintenance_after_years=11,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='swearingkevo-class-52.wav',
    constraint_prev=['none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/br-cl52-maroon.blend',
    upstream_dat='trains/br-cl52.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
