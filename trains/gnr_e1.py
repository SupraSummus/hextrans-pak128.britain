"""gnr-e1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/E/e1.php
SPEC = Vehicle(
    name='gnr-e1',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1897,
    intro_month=6,
    retire_year=1902,
    retire_month=3,
    speed=125,
    length=5,
    weight=42.1,
    axle_load=15,
    power=198,
    tractive_effort=61,
    payload=0,
    cost=9000000,
    runningcost=133,
    fixed_cost=31500,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['GNR-C1-Tender'],
    liverytype=['GNR-Standard', 'LNER-Standard'],
    blend='trains/Locomotives/gnr-e1-class.blend',
    upstream_dat='trains/gnr-e1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
