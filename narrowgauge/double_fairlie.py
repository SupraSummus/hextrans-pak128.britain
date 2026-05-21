"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='DoubleFairlie',
    waytype='narrowgauge_track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1872,
    intro_month=12,
    retire_year=1910,
    retire_month=10,
    speed=60,
    length=6,
    weight=24.3,
    axle_load=5,
    power=60,
    tractive_effort=27,
    rolling_resistance=19,
    payload=0,
    cost=3237692,
    runningcost=54,
    fixed_cost=18698,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='the-mart-ban-double-fairlie.wav',
    liverytype=['FR-Royal-Purple', 'FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Cherry-Red'],
    upgrade=['DoubleFairlie-superheated'],
    blend='narrowgauge/double-fairlie-maroon.blend',
    upstream_dat='narrowgauge/double-fairlie.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
