"""br-cl45."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class45',
    waytype='track',
    copyright='Kieron/jamespetts',
    freight='None',
    engine_type='diesel',
    intro_year=1960,
    intro_month=3,
    retire_year=1963,
    retire_month=1,
    speed=145,
    length=12,
    weight=136,
    axles=8,
    power=1864,
    gear=50,
    tractive_effort=245,
    rolling_resistance=13,
    payload=0,
    cost=12000000,
    runningcost=934,
    fixed_cost=18333,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='russell-thewils-class-46.wav',
    constraint_prev=['BR-Class15', 'BR-Class17', 'BR-Class20', 'BR-Class24', 'BR-Class25', 'BR-Class26', 'BR-Class27', 'BR-Class31-1', 'BR-Class37', 'BR-Class40', 'BR-Class45', 'none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/br-cl45-green.blend',
    upstream_dat='trains/br-cl45.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
