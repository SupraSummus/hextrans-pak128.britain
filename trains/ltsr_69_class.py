"""ltsr-69-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='ltsr-69-class',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1903,
    intro_month=4,
    retire_year=1913,
    retire_month=3,
    speed=95,
    length=6,
    weight=65.7,
    axle_load=17,
    power=288,
    tractive_effort=86,
    payload=0,
    cost=8200000,
    runningcost=124,
    fixed_cost=46833,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LTSR-standard', 'MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/ltsr-69-class-br.blend',
    upstream_dat='trains/ltsr-69-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
