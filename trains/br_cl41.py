"""br-cl41."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class41',
    waytype='track',
    copyright='Junna/Cake',
    freight='None',
    engine_type='diesel',
    intro_year=1958,
    intro_month=1,
    retire_year=1959,
    retire_month=12,
    speed=145,
    length=11,
    weight=119,
    axles=6,
    power=1492,
    gear=50,
    tractive_effort=222,
    rolling_resistance=13,
    payload=0,
    cost=1520000,
    runningcost=1492,
    fixed_cost=11583,
    increase_maintenance_after_years=23,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='spompeytransportvideo-class-42.wav',
    constraint_prev=['BR-Class41', 'none'],
    liverytype=['BR-Early', 'BR-Blue'],
    blend='trains/Locomotives/br-cl41-newgreen.blend',
    upstream_dat='trains/br-cl41.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
