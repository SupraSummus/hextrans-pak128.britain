"""lnwr-experiment."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-Experiment',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1904,
    intro_month=3,
    retire_year=1911,
    retire_month=6,
    speed=143,
    length=6,
    weight=66.8,
    axle_load=18,
    power=330,
    tractive_effort=83,
    payload=0,
    cost=99000000,
    runningcost=157,
    fixed_cost=122500,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-PrinceOfWales-Tender'],
    liverytype=['LNWR-Black', 'LMS-Standard'],
    blend='trains/Locomotives/lnwr-experiment-lms.blend',
    upstream_dat='trains/lnwr-experiment.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
