"""secr-n1-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SECR-N1-Class',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1922,
    intro_month=12,
    retire_year=1934,
    retire_month=11,
    speed=107,
    length=6,
    weight=64,
    axle_load=18,
    power=362,
    tractive_effort=123,
    way_wear_factor=88000,
    payload=0,
    cost=7400000,
    runningcost=198,
    fixed_cost=46167,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['SECR-N-Class-Tender'],
    liverytype=['WW1-Austerity', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/secr-n1-class-ww1-austerity.blend',
    upstream_dat='trains/secr-n1-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
