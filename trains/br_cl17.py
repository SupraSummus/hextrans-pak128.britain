"""br-cl17."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class17',
    waytype='track',
    copyright='Junna/Cake',
    freight='None',
    engine_type='diesel',
    intro_year=1962,
    intro_month=2,
    retire_year=1965,
    retire_month=10,
    speed=97,
    length=8,
    weight=70,
    axles=4,
    power=671,
    gear=50,
    tractive_effort=178,
    rolling_resistance=13,
    payload=0,
    cost=7056000,
    runningcost=336,
    fixed_cost=14900,
    increase_maintenance_after_years=11,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='androo4519-class-17.wav',
    constraint_prev=['BR-Class17', 'none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/br-cl17-b.blend',
    upstream_dat='trains/br-cl17.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
