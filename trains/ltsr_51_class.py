"""ltsr-51-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='ltsr-51-class',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1900,
    intro_month=1,
    retire_year=1911,
    retire_month=2,
    speed=125,
    length=6,
    weight=68.9,
    axle_load=18,
    power=282,
    tractive_effort=69,
    payload=0,
    cost=8210000,
    runningcost=142,
    fixed_cost=46842,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LTSR-standard', 'MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/ltsr-51-class-br.blend',
    upstream_dat='trains/ltsr-51-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
