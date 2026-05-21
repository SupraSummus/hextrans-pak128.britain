"""br-cl55."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class55',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='diesel',
    intro_year=1961,
    intro_month=9,
    retire_year=1967,
    retire_month=12,
    speed=160,
    length=12,
    weight=101,
    axles=6,
    power=2460,
    gear=50,
    tractive_effort=222,
    rolling_resistance=13,
    payload=0,
    cost=13364000,
    runningcost=1232,
    fixed_cost=19281,
    increase_maintenance_after_years=15,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='video47-class-55.wav',
    constraint_prev=['none'],
    liverytype=['BR-Early', 'BR-Blue', 'BR-Large-Logo'],
    blend='trains/Locomotives/br-cl55-large-logo.blend',
    upstream_dat='trains/br-cl55.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
