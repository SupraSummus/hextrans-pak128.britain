"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'air/junkers-f13.blend'
_UPSTREAM_DAT = 'air/junkers-f13.dat'

SPECS = [
Vehicle(
    name='junkers-f13',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Passagiere',
    engine_type='petrol',
    intro_year=1920,
    intro_month=4,
    retire_year=1932,
    retire_month=6,
    speed=160,
    weight=1.1,
    power=126,
    tractive_effort=2,
    payload=4,
    min_loading_time=1550,
    max_loading_time=1550,
    catering_level=0,
    cost=1000000,
    runningcost=6,
    fixed_cost=50694,
    sound='planelow.wav',
    minimum_runway_length=200,
    range=1200,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 0, 0, 4],
    comfort_by_class=[0, 0, 0, 0, 66],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='junkers-f13-mail',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Post',
    engine_type='petrol',
    intro_year=1920,
    intro_month=4,
    retire_year=1932,
    retire_month=6,
    speed=160,
    weight=1.1,
    power=126,
    tractive_effort=2,
    payload=650,
    min_loading_time=1550,
    max_loading_time=1750,
    cost=1000000,
    runningcost=6,
    fixed_cost=10694,
    sound='planelow.wav',
    minimum_runway_length=200,
    range=1200,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 650],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
