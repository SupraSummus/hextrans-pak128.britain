"""mr-25."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-25',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1887,
    intro_month=8,
    retire_year=1896,
    retire_month=4,
    speed=145,
    length=5,
    weight=40,
    axle_load=17,
    power=244,
    tractive_effort=54,
    payload=0,
    cost=5015500,
    runningcost=163,
    fixed_cost=28180,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-Kirtley156Tender'],
    blend='trains/Locomotives/mr-25-class.blend',
    upstream_dat='trains/mr-25.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
