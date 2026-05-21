"""br-cl24."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class24',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='diesel',
    intro_year=1958,
    intro_month=1,
    retire_year=1961,
    retire_month=11,
    speed=121,
    length=9,
    weight=74,
    axles=4,
    power=865,
    gear=50,
    tractive_effort=187,
    rolling_resistance=13,
    payload=0,
    cost=8650000,
    runningcost=867,
    fixed_cost=19010,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='the-mart-ban-class-25.wav',
    constraint_prev=['BR-Class15', 'BR-Class17', 'BR-Class20', 'BR-Class24', 'BR-Class25', 'BR-Class26', 'BR-Class27', 'BR-Class31-1', 'BR-Class37', 'BR-Class40', 'BR-Class45', 'none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/br-cl24-green.blend',
    upstream_dat='trains/br-cl24.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
