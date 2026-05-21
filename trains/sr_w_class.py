"""sr-w-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='sr-w-class',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1930,
    intro_month=2,
    retire_year=1936,
    retire_month=12,
    speed=95,
    length=8,
    weight=92.2,
    axle_load=19,
    power=363,
    tractive_effort=131,
    payload=0,
    cost=3950000,
    runningcost=212,
    fixed_cost=27292,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/sr-w-class-austerity.blend',
    upstream_dat='trains/sr-w-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
