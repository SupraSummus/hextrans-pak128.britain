"""lner-l1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/L/l1thompson.php
SPEC = Vehicle(
    name='lner-l1',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1945,
    intro_month=5,
    retire_year=1952,
    retire_month=7,
    speed=105,
    length=7,
    weight=90.8,
    axle_load=20,
    power=359,
    tractive_effort=142,
    payload=0,
    cost=9534525,
    runningcost=113,
    fixed_cost=49752,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LNER-Standard', 'BR-Early'],
    blend='trains/Locomotives/lner-l1-br.blend',
    upstream_dat='trains/lner-l1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
