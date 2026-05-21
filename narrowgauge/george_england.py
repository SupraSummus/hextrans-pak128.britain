"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'narrowgauge/george-england-maroon.blend'
_UPSTREAM_DAT = 'narrowgauge/george-england.dat'

SPECS = [
Vehicle(
    name='George-England',
    waytype='narrowgauge_track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1863,
    intro_month=8,
    retire_year=1876,
    retire_month=12,
    speed=45,
    length=3,
    weight=6.6,
    axle_load=3,
    power=14,
    tractive_effort=17,
    rolling_resistance=20,
    payload=0,
    cost=1726769,
    runningcost=11,
    fixed_cost=17439,
    bidirectional=0,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='the-mart-ban-wllr-tank.wav',
    constraint_next=['George-England-tender'],
    liverytype=['FR-Royal-Purple', 'FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Cherry-Red'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='George-England-tender',
    waytype='narrowgauge_track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1863,
    intro_month=8,
    retire_year=1876,
    retire_month=12,
    speed=45,
    length=2,
    weight=3,
    axles=2,
    power=0,
    rolling_resistance=20,
    payload=0,
    cost=0,
    runningcost=0,
    bidirectional=0,
    can_lead_from_rear=0,
    constraint_prev=['George-England'],
    liverytype=['FR-Royal-Purple', 'FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Cherry-Red'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
