"""br-cl60."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class60',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='diesel',
    intro_year=1989,
    intro_month=9,
    retire_year=1998,
    retire_month=9,
    speed=97,
    length=12,
    weight=129,
    axles=6,
    power=2300,
    gear=50,
    tractive_effort=474,
    brake_force=96,
    rolling_resistance=13,
    payload=0,
    cost=8206000,
    runningcost=691,
    fixed_cost=14274,
    increase_maintenance_after_years=20,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='treacher-rail-class-60.wav',
    constraint_prev=['BR-Class60', 'none'],
    blend='trains/Locomotives/br-cl60-rf.blend',
    upstream_dat='trains/br-cl60.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
