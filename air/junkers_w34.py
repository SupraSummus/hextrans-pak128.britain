"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'air/junkers-w34.blend'
_UPSTREAM_DAT = 'air/junkers-w34.dat'

SPECS = [
Vehicle(
    name='junkers-w34',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Passagiere',
    engine_type='petrol',
    intro_year=1926,
    intro_month=7,
    retire_year=1935,
    retire_month=9,
    speed=190,
    weight=1.9,
    power=298,
    tractive_effort=4,
    payload=6,
    min_loading_time=1600,
    max_loading_time=1600,
    catering_level=0,
    cost=1750000,
    runningcost=15,
    fixed_cost=51215,
    sound='planelow.wav',
    minimum_runway_length=300,
    range=900,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 0, 0, 6],
    comfort_by_class=[0, 0, 0, 0, 66],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='junkers-w34-mail',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Post',
    engine_type='petrol',
    intro_year=1926,
    intro_month=7,
    retire_year=1935,
    retire_month=9,
    speed=190,
    weight=1.9,
    power=298,
    tractive_effort=4,
    payload=1100,
    min_loading_time=1600,
    max_loading_time=1800,
    cost=1750000,
    runningcost=15,
    fixed_cost=11215,
    sound='planelow.wav',
    minimum_runway_length=300,
    range=900,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 1100],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
