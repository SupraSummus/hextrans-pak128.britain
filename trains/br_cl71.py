"""br-cl71."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class71',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='electric',
    intro_year=1958,
    intro_month=9,
    retire_year=1964,
    retire_month=12,
    speed=145,
    length=9,
    weight=77,
    axles=4,
    power=1720,
    gear=80,
    tractive_effort=195,
    rolling_resistance=13,
    payload=0,
    cost=4032000,
    runningcost=345,
    fixed_cost=12800,
    increase_maintenance_after_years=21,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='antman09ful1-class-71.wav',
    constraint_prev=['none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    way_constraint_permissive=[0],
    blend='trains/Locomotives/br-cl71-blue.blend',
    upstream_dat='trains/br-cl71.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
