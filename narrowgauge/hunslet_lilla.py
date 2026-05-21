"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='hunslet-lilla',
    waytype='narrowgauge_track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1891,
    intro_month=7,
    retire_year=1955,
    retire_month=10,
    speed=40,
    length=4,
    weight=10.9,
    axles=2,
    power=18,
    tractive_effort=21,
    rolling_resistance=18,
    payload=0,
    cost=2015326,
    runningcost=13,
    fixed_cost=17300,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='laurie-barclay-0-4-0.wav',
    liverytype=['FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Cherry-Red'],
    blend='narrowgauge/hunslet-lilla-scarlet.blend',
    upstream_dat='narrowgauge/hunslet-lilla.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
