"""br-cl42."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class42',
    waytype='track',
    copyright='Junna/Cake',
    freight='None',
    engine_type='diesel',
    intro_year=1958,
    intro_month=4,
    retire_year=1962,
    retire_month=11,
    speed=145,
    length=11,
    weight=79,
    axles=4,
    power=1692,
    gear=50,
    tractive_effort=214,
    rolling_resistance=13,
    payload=0,
    cost=1620000,
    runningcost=1692,
    fixed_cost=11688,
    increase_maintenance_after_years=23,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='spompeytransportvideo-class-42.wav',
    constraint_prev=['BR-Class42', 'none'],
    liverytype=['BR-Early', 'BR-Blue'],
    blend='trains/Locomotives/br-cl42-blue.blend',
    upstream_dat='trains/br-cl42.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
