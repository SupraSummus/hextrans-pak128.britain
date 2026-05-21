"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='hunslet-quarry',
    waytype='narrowgauge_track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1870,
    intro_month=5,
    retire_year=1889,
    retire_month=7,
    speed=35,
    length=2,
    weight=4.8,
    axles=2,
    power=9,
    tractive_effort=7,
    rolling_resistance=20,
    payload=0,
    cost=1395226,
    runningcost=8,
    fixed_cost=17292,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='laurie-barclay-0-4-0.wav',
    liverytype=['FR-Royal-Purple', 'FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Cherry-Red'],
    blend='narrowgauge/hunslet-quarry-maroon.blend',
    upstream_dat='narrowgauge/hunslet-quarry.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
