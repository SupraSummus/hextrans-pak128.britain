"""secr-k-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='secr-k-class',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1917,
    intro_month=7,
    retire_year=1927,
    retire_month=12,
    speed=100,
    length=7,
    weight=83.9,
    axle_load=19,
    power=368,
    tractive_effort=106,
    payload=0,
    cost=7650900,
    runningcost=200,
    fixed_cost=30376,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['WW1-Austerity', 'SR-Olive-Green'],
    blend='trains/Locomotives/secr-k-class-olive.blend',
    upstream_dat='trains/secr-k-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
