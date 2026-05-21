"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'air/lockheed-vega.blend'
_UPSTREAM_DAT = 'air/lockheed-vega.dat'

SPECS = [
Vehicle(
    name='lockheed-vega',
    waytype='air',
    copyright='Emmanuel Baranger and Самолеты',
    freight='Passagiere',
    engine_type='petrol',
    intro_year=1928,
    intro_month=3,
    retire_year=1933,
    retire_month=1,
    speed=285,
    weight=1.5,
    power=302,
    tractive_effort=3,
    payload=6,
    min_loading_time=1600,
    max_loading_time=1600,
    catering_level=1,
    cost=2290000,
    runningcost=15,
    fixed_cost=51590,
    sound='planelow.wav',
    minimum_runway_length=350,
    range=1165,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 0, 0, 6],
    comfort_by_class=[0, 0, 0, 0, 65],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='lockheed-vega-mail',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Post',
    engine_type='petrol',
    intro_year=1928,
    intro_month=3,
    retire_year=1933,
    retire_month=1,
    speed=285,
    weight=1.5,
    power=302,
    tractive_effort=3,
    payload=1500,
    min_loading_time=1600,
    max_loading_time=2000,
    comfort=65,
    cost=2290000,
    runningcost=15,
    fixed_cost=11590,
    sound='planelow.wav',
    minimum_runway_length=500,
    range=1165,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 1500],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
