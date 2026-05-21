"""br-121."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-121',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='Passagiere',
    engine_type='diesel',
    intro_year=1960,
    intro_month=4,
    retire_year=1980,
    retire_month=11,
    speed=112,
    length=11,
    weight=38.0,
    axles=4,
    power=224,
    gear=50,
    tractive_effort=32,
    payload=65,
    min_loading_time=12,
    max_loading_time=43,
    overcrowded_capacity=66,
    cost=1300000,
    runningcost=112,
    fixed_cost=10903,
    increase_maintenance_after_years=10,
    bidirectional=1,
    can_lead_from_rear=1,
    smoke='Diesel',
    sound='spompeytransportvideo-class-117.wav',
    constraint_prev=['BR-121', 'BR-117-DMS', 'BR-104Rear', 'BR-128', 'BR-101-DMCL', 'BR-101-DTCL', 'BR-114-DTCL', 'BR-120-DMSL', 'BR-110-DMCL', 'none'],
    constraint_next=['BR-121', 'BR-117-DMBS', 'BR-104Front', 'BR-128', 'BR-101-DMBS', 'BR-120-DMBC', 'BR-114-DMBS', 'BR-110-DMBC', 'none'],
    payload_by_class=[0, 65],
    comfort_by_class=[0, 75],
    liverytype=['BR-Revised', 'BR-Blue', 'BR-Large-Logo', 'NSE-Standard', 'Regional-Railways-Standard'],
    blend='trains/Railcars/br-121-nse-new.blend',
    upstream_dat='trains/br-121.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
