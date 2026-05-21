"""mr-1738."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-1738',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1885,
    intro_month=6,
    retire_year=1893,
    retire_month=6,
    speed=140,
    length=5,
    weight=43,
    axle_load=14,
    power=221,
    tractive_effort=58,
    payload=0,
    cost=5935000,
    runningcost=148,
    fixed_cost=28946,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-Kirtley156Tender'],
    upgrade=['MR-483'],
    blend='trains/Locomotives/mr-1738-class-green.blend',
    upstream_dat='trains/mr-1738.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
