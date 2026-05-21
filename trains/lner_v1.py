"""lner-v1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/V/v1v3.php
# https://en.wikipedia.org/wiki/LNER_Class_V1/V3
SPEC = Vehicle(
    name='lner-v1',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1930,
    intro_month=4,
    retire_year=1939,
    retire_month=5,
    speed=108,
    length=7,
    weight=57.9,
    axle_load=19,
    power=313,
    tractive_effort=100,
    payload=0,
    cost=8527525,
    runningcost=95,
    fixed_cost=42005,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early'],
    upgrade=['lner-v3'],
    blend='trains/Locomotives/lner-v1-austerity.blend',
    upstream_dat='trains/lner-v1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
