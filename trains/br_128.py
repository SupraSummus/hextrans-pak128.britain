"""br-128."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-128',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='Post',
    engine_type='diesel',
    intro_year=1959,
    intro_month=7,
    retire_year=1980,
    retire_month=10,
    speed=112,
    length=11,
    weight=38,
    axles=4,
    power=343,
    gear=50,
    tractive_effort=32,
    payload=480,
    min_loading_time=25,
    max_loading_time=200,
    cost=1340000,
    runningcost=343,
    fixed_cost=11396,
    increase_maintenance_after_years=10,
    bidirectional=1,
    can_lead_from_rear=1,
    smoke='Diesel',
    sound='spompeytransportvideo-class-117.wav',
    constraint_prev=['BR-121', 'BR-117-DMS', 'BR-104Rear', 'BR-128', 'BR-101-DMCL', 'BR-101-DTCL', 'BR-114-DTCL', 'BR-120-DMSL', 'BR-110-DMCL', 'none'],
    constraint_next=['BR-121', 'BR-117-DMBS', 'BR-104Front', 'BR-128', 'BR-101-DMBS', 'BR-120-DMBC', 'BR-114-DMBS', 'BR-110-DMBC', 'none'],
    liverytype=['BR-Revised', 'BR-Blue', 'RM-Revised'],
    blend='trains/Railcars/br-128-rm-revised.blend',
    upstream_dat='trains/br-128.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
