"""br-cl25."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class25',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='diesel',
    intro_year=1961,
    intro_month=11,
    retire_year=1974,
    retire_month=6,
    speed=145,
    length=9,
    weight=72,
    axles=4,
    power=932,
    gear=50,
    tractive_effort=173,
    rolling_resistance=13,
    payload=0,
    cost=8870000,
    runningcost=467,
    fixed_cost=16160,
    increase_maintenance_after_years=14,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='the-mart-ban-class-25.wav',
    constraint_prev=['BR-Class15', 'BR-Class17', 'BR-Class20', 'BR-Class24', 'BR-Class25', 'BR-Class26', 'BR-Class27', 'BR-Class31-1', 'BR-Class37', 'BR-Class40', 'BR-Class45', 'none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/br-cl25-green.blend',
    upstream_dat='trains/br-cl25.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
