"""lms-10800."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Built by the North British company for the LMS, but delivered in BR days.
# https://en.wikipedia.org/wiki/British_Rail_10800
SPEC = Vehicle(
    name='BR-Class10800',
    waytype='track',
    copyright='Junna/Cake/JamesPetts',
    freight='None',
    engine_type='diesel',
    intro_year=1950,
    intro_month=7,
    retire_year=1957,
    retire_month=11,
    speed=110,
    length=8,
    weight=70.9,
    axles=4,
    power=617,
    gear=50,
    tractive_effort=153,
    brake_force=45,
    rolling_resistance=13,
    payload=0,
    cost=3935000,
    runningcost=618,
    fixed_cost=14099,
    increase_maintenance_after_years=15,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='androo4519-class-17.wav',
    constraint_prev=['none'],
    liverytype=['BR-Early', 'BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/10800.blend',
    upstream_dat='trains/lms-10800.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
