"""br-cl40."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class40',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='diesel',
    intro_year=1958,
    intro_month=9,
    retire_year=1962,
    retire_month=2,
    speed=145,
    length=12,
    weight=136,
    axles=8,
    power=1490,
    gear=50,
    tractive_effort=231,
    rolling_resistance=13,
    payload=0,
    cost=10598000,
    runningcost=1493,
    fixed_cost=21040,
    increase_maintenance_after_years=22,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='lwalker-class-40.wav',
    constraint_prev=['BR-Class15', 'BR-Class17', 'BR-Class20', 'BR-Class24', 'BR-Class25', 'BR-Class26', 'BR-Class27', 'BR-Class31-1', 'BR-Class37', 'BR-Class40', 'BR-Class45', 'none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/br-cl40-green.blend',
    upstream_dat='trains/br-cl40.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
