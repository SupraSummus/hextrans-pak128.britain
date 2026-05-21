"""br-cl35."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class35',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='diesel',
    intro_year=1961,
    intro_month=2,
    retire_year=1965,
    retire_month=10,
    speed=145,
    length=9,
    weight=74,
    axles=4,
    power=1305,
    gear=50,
    tractive_effort=207,
    rolling_resistance=13,
    payload=0,
    cost=7056000,
    runningcost=653,
    fixed_cost=14900,
    increase_maintenance_after_years=11,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='treacher-rail-class-35.wav',
    constraint_prev=['BR-Class35', 'none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/br-cl35-green.blend',
    upstream_dat='trains/br-cl35.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
