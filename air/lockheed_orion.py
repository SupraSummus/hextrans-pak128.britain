"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'air/lockheed-orion.blend'
_UPSTREAM_DAT = 'air/lockheed-orion.dat'

SPECS = [
Vehicle(
    name='lockheed-orion',
    waytype='air',
    copyright='Cadnav',
    freight='Passagiere',
    engine_type='petrol',
    intro_year=1931,
    intro_month=5,
    retire_year=1934,
    retire_month=4,
    speed=282,
    weight=1.9,
    power=386,
    tractive_effort=4,
    payload=6,
    min_loading_time=1600,
    max_loading_time=1600,
    catering_level=1,
    cost=2300000,
    runningcost=22,
    fixed_cost=51597,
    sound='planelow.wav',
    minimum_runway_length=345,
    range=1159,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 0, 0, 6],
    comfort_by_class=[0, 0, 0, 0, 67],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='lockheed-orion-mail',
    waytype='air',
    copyright='Cadnav',
    freight='Post',
    engine_type='petrol',
    intro_year=1931,
    intro_month=5,
    retire_year=1934,
    retire_month=4,
    speed=282,
    weight=1.9,
    power=386,
    tractive_effort=4,
    payload=1500,
    min_loading_time=1600,
    max_loading_time=1600,
    cost=2300000,
    runningcost=22,
    fixed_cost=11597,
    sound='planelow.wav',
    minimum_runway_length=345,
    range=1159,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 1500],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
