"""gnr-c12-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/C/c12.php
SPEC = Vehicle(
    name='gnr-c12-class',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1898,
    intro_month=2,
    retire_year=1908,
    retire_month=3,
    speed=103,
    length=6,
    weight=40.4,
    axle_load=17,
    power=218,
    tractive_effort=67,
    payload=0,
    cost=6510000,
    runningcost=145,
    fixed_cost=28105,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['GNR-Standard', 'LNER-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gnr-c12-class-austerity.blend',
    upstream_dat='trains/gnr-c12-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
