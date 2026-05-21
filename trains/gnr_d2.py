"""gnr-d2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gnr-d2',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1896,
    intro_month=1,
    retire_year=1899,
    retire_month=6,
    speed=130,
    length=5,
    weight=46.4,
    axle_load=15,
    power=199,
    tractive_effort=63,
    payload=0,
    cost=9250000,
    runningcost=134,
    fixed_cost=31708,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['GNR-C1-Tender'],
    liverytype=['GNR-Standard', 'LNER-Standard'],
    blend='trains/Locomotives/gnr-d2-class-lner.blend',
    upstream_dat='trains/gnr-d2.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
