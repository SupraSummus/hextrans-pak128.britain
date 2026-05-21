"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'air/boeing-737-700.blend'
_UPSTREAM_DAT = 'air/boeing-737-700.dat'

SPECS = [
Vehicle(
    name='boeing-737-700',
    waytype='air',
    copyright='kaichinshih',
    freight='Passagiere',
    engine_type='turbine',
    intro_year=1997,
    intro_month=12,
    retire_year=2020,
    retire_month=7,
    speed=833,
    weight=38.1,
    power=32040,
    tractive_effort=178,
    payload=120,
    min_loading_time=2400,
    max_loading_time=2400,
    catering_level=2,
    cost=48900000,
    runningcost=128,
    fixed_cost=83958,
    upgrade_price=5000,
    sound='laxspotter97-boeing737-800.wav',
    minimum_runway_length=2140,
    range=5570,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 120, 0, 8, 0],
    comfort_by_class=[0, 137, 0, 154],
    upgrade=['boeing-737-700-high-density'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='boeing-737-700-high-density',
    waytype='air',
    copyright='kaichinshih',
    freight='Passagiere',
    engine_type='turbine',
    intro_year=1997,
    intro_month=12,
    retire_year=2020,
    retire_month=7,
    speed=833,
    weight=38.1,
    power=32040,
    tractive_effort=178,
    payload=148,
    min_loading_time=2400,
    max_loading_time=2400,
    catering_level=1,
    cost=48900000,
    runningcost=128,
    fixed_cost=83958,
    upgrade_price=5000,
    sound='laxspotter97-boeing737-800.wav',
    minimum_runway_length=2140,
    range=5570,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[148],
    comfort_by_class=[121],
    upgrade=['boeing-737-700'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
