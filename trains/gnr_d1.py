"""gnr-d1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gnr-d1',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1911,
    intro_month=3,
    retire_year=1918,
    retire_month=6,
    speed=130,
    length=5,
    weight=54.2,
    axle_load=18,
    power=270,
    tractive_effort=72,
    payload=0,
    cost=9450000,
    runningcost=113,
    fixed_cost=31875,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['GNR-C1-Tender'],
    liverytype=['GNR-Standard', 'LNER-Standard'],
    blend='trains/Locomotives/gnr-d1-class-lner.blend',
    upstream_dat='trains/gnr-d1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
