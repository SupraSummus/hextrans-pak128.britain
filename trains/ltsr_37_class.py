"""ltsr-37-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='ltsr-37-class',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1897,
    intro_month=1,
    retire_year=1910,
    retire_month=1,
    speed=122,
    length=6,
    weight=72.9,
    axle_load=18,
    power=273,
    tractive_effort=77,
    payload=0,
    cost=8200000,
    runningcost=183,
    fixed_cost=30833,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LTSR-standard', 'MR-Standard', 'LMS-Standard'],
    blend='trains/Locomotives/ltsr-37-class-lms.blend',
    upstream_dat='trains/ltsr-37-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
