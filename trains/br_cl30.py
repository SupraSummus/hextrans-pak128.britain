"""br-cl30."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class30',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='diesel',
    intro_year=1957,
    intro_month=9,
    retire_year=1963,
    retire_month=11,
    speed=130,
    length=10,
    weight=107,
    axles=6,
    power=930,
    gear=50,
    tractive_effort=120,
    rolling_resistance=13,
    payload=0,
    cost=8870000,
    runningcost=932,
    fixed_cost=19240,
    increase_maintenance_after_years=6,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='laurie-class-31.wav',
    constraint_prev=['BR-Class16', 'BR-Class21', 'BR-Class28', 'BR-Class29', 'BR-Class30', 'none'],
    upgrade=['BR-Class31-1'],
    blend='trains/Locomotives/br-cl30-green.blend',
    upstream_dat='trains/br-cl30.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
