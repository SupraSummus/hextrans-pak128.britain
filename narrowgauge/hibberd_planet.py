"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Hibberd-Planet',
    waytype='narrowgauge_track',
    copyright='James',
    freight='None',
    engine_type='diesel',
    intro_year=1954,
    intro_month=11,
    retire_year=1987,
    retire_month=9,
    speed=60,
    length=3,
    weight=19,
    axles=2,
    power=134,
    gear=50,
    tractive_effort=45,
    rolling_resistance=18,
    payload=0,
    cost=8993590,
    runningcost=136,
    fixed_cost=19368,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='video47-ng-diesel.wav',
    blend='narrowgauge/hibberd-planet.blend',
    upstream_dat='narrowgauge/hibberd-planet.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
