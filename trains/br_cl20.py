"""br-cl20."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class20',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='diesel',
    intro_year=1957,
    intro_month=9,
    retire_year=1968,
    retire_month=10,
    speed=120,
    length=8,
    weight=73.2,
    axles=4,
    power=746,
    gear=50,
    tractive_effort=186,
    rolling_resistance=13,
    payload=0,
    cost=4435000,
    runningcost=747,
    fixed_cost=14620,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='laurie-class-20.wav',
    constraint_prev=['BR-Class15', 'BR-Class17', 'BR-Class20', 'BR-Class24', 'BR-Class25', 'BR-Class26', 'BR-Class27', 'BR-Class31-1', 'BR-Class37', 'BR-Class40', 'BR-Class45', 'none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/br-cl20-green.blend',
    upstream_dat='trains/br-cl20.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
