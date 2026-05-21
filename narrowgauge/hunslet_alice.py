"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Hunslet-Alice',
    waytype='narrowgauge_track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1886,
    intro_month=2,
    retire_year=1917,
    retire_month=10,
    speed=40,
    length=3,
    weight=6.1,
    axles=2,
    power=13,
    tractive_effort=11,
    rolling_resistance=19,
    payload=0,
    cost=1550251,
    runningcost=10,
    fixed_cost=17292,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='laurie-barclay-0-4-0.wav',
    liverytype=['FR-Royal-Purple', 'FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Cherry-Red'],
    blend='narrowgauge/hunslet-alice-maroon.blend',
    upstream_dat='narrowgauge/hunslet-alice.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
