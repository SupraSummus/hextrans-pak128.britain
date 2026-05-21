"""mr-2736."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-2736',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1903,
    intro_month=5,
    retire_year=1911,
    retire_month=6,
    speed=85,
    length=4,
    weight=43,
    axles=3,
    power=191,
    tractive_effort=86,
    payload=0,
    cost=7616000,
    runningcost=83,
    fixed_cost=30347,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-483-Tender'],
    liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/mr-2736-lms.blend',
    upstream_dat='trains/mr-2736.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
