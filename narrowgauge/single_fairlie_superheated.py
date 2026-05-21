"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SingleFairlie-superheated',
    waytype='narrowgauge_track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1910,
    intro_month=10,
    retire_year=1954,
    retire_month=11,
    speed=60,
    length=4,
    weight=16,
    axle_load=6,
    power=46,
    tractive_effort=24,
    rolling_resistance=19,
    payload=0,
    cost=3597436,
    runningcost=34,
    fixed_cost=18998,
    upgrade_price=719487,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='the-mart-ban-wllr-tank.wav',
    liverytype=['FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Cherry-Red'],
    blend='narrowgauge/single-fairlie-superheated.blend',
    upstream_dat='narrowgauge/single-fairlie-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
