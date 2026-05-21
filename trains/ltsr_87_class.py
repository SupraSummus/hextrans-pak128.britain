"""ltsr-87-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='ltsr-87-class',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1912,
    intro_month=6,
    retire_year=1930,
    retire_month=8,
    speed=130,
    length=8,
    weight=96.1,
    axle_load=18,
    power=392,
    tractive_effort=84,
    payload=0,
    cost=7700000,
    runningcost=164,
    fixed_cost=46417,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LTSR-standard', 'MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/ltsr-87-class.blend',
    upstream_dat='trains/ltsr-87-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
