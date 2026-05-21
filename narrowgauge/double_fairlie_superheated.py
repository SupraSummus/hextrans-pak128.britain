"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='DoubleFairlie-superheated',
    waytype='narrowgauge_track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1910,
    intro_month=10,
    retire_year=1958,
    retire_month=7,
    speed=60,
    length=6,
    weight=31.5,
    axle_load=7,
    power=95,
    tractive_effort=43,
    rolling_resistance=19,
    payload=0,
    cost=5396154,
    runningcost=64,
    fixed_cost=20497,
    upgrade_price=1079231,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='the-mart-ban-double-fairlie.wav',
    liverytype=['FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Cherry-Red'],
    blend='narrowgauge/double-fairlie-superheated.blend',
    upstream_dat='narrowgauge/double-fairlie-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
