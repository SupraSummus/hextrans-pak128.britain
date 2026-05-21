"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'air/boeing-247.blend'
_UPSTREAM_DAT = 'air/boeing-247.dat'

SPECS = [
Vehicle(
    name='boeing-247',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Passagiere',
    engine_type='petrol',
    intro_year=1933,
    intro_month=5,
    retire_year=1938,
    retire_month=8,
    speed=304,
    weight=4.5,
    power=738,
    tractive_effort=7,
    payload=10,
    min_loading_time=1800,
    max_loading_time=1800,
    catering_level=1,
    cost=2250000,
    runningcost=37,
    fixed_cost=51563,
    sound='ylearkisto-dc-3.wav',
    minimum_runway_length=500,
    range=1200,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 0, 0, 10],
    comfort_by_class=[0, 0, 0, 0, 80],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='boeing-247-mail',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Post',
    engine_type='petrol',
    intro_year=1933,
    intro_month=5,
    retire_year=1938,
    retire_month=8,
    speed=304,
    weight=4.5,
    power=738,
    tractive_effort=7,
    payload=1600,
    min_loading_time=1800,
    max_loading_time=2000,
    cost=2250000,
    runningcost=37,
    fixed_cost=11563,
    sound='ylearkisto-dc-3.wav',
    minimum_runway_length=500,
    range=1200,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 1600],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
