"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SingleFairlie',
    waytype='narrowgauge_track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1876,
    intro_month=12,
    retire_year=1910,
    retire_month=10,
    speed=55,
    length=4,
    weight=14.2,
    axle_load=5,
    power=34,
    tractive_effort=17,
    rolling_resistance=19,
    payload=0,
    cost=2877949,
    runningcost=25,
    fixed_cost=18398,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='the-mart-ban-wllr-tank.wav',
    liverytype=['FR-Royal-Purple', 'FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Cherry-Red'],
    upgrade=['SingleFairlie-superheated'],
    blend='narrowgauge/single-fairlie-maroon.blend',
    upstream_dat='narrowgauge/single-fairlie.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
