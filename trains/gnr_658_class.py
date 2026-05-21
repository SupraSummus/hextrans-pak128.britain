"""gnr-658-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.gnrsociety.com/locomotive-class/658-class/
# https://www.lner.info/locos/G/g2.php
SPEC = Vehicle(
    name='gnr-658-class',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1881,
    intro_month=7,
    retire_year=1892,
    retire_month=4,
    speed=88,
    length=6,
    weight=51.6,
    axle_load=17,
    power=197,
    tractive_effort=67,
    payload=0,
    cost=3580000,
    runningcost=106,
    fixed_cost=26800,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['GNR-Standard', 'LNER-Standard'],
    blend='trains/Locomotives/gnr-658-class-lner.blend',
    upstream_dat='trains/gnr-658-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
