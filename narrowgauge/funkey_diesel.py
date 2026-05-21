"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Funkey-Deisel',
    waytype='narrowgauge_track',
    copyright='James',
    freight='None',
    engine_type='diesel',
    intro_year=1968,
    intro_month=6,
    speed=60,
    length=5,
    weight=27.4,
    axles=4,
    power=265,
    gear=50,
    tractive_effort=72,
    rolling_resistance=18,
    payload=0,
    cost=13490385,
    runningcost=134,
    fixed_cost=19368,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='video47-ng-diesel.wav',
    blend='narrowgauge/funkey-diesel.blend',
    upstream_dat='narrowgauge/funkey-diesel.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
