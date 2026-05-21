"""ltsr-79-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='ltsr-79-class',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1909,
    intro_month=2,
    retire_year=1930,
    retire_month=8,
    speed=130,
    length=6,
    weight=72.7,
    axle_load=20,
    power=287,
    tractive_effort=77,
    payload=0,
    cost=8440000,
    runningcost=127,
    fixed_cost=31033,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    liverytype=['LTSR-standard', 'MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/ltsr-79-class-br.blend',
    upstream_dat='trains/ltsr-79-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
