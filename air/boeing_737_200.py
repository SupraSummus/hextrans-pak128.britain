"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'air/boeing-737-200.blend'
_UPSTREAM_DAT = 'air/boeing-737-200.dat'

SPECS = [
Vehicle(
    name='boeing-737-200',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Passagiere',
    engine_type='turbine',
    intro_year=1968,
    intro_month=2,
    retire_year=1988,
    retire_month=8,
    speed=778,
    weight=27.4,
    power=25560,
    tractive_effort=142,
    payload=73,
    min_loading_time=2400,
    max_loading_time=2400,
    catering_level=2,
    cost=40000000,
    runningcost=154,
    fixed_cost=77778,
    sound='laxspotter97-boeing737-200.wav',
    minimum_runway_length=2189,
    range=3520,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 73, 0, 24],
    comfort_by_class=[0, 0, 105, 0, 170],
    upgrade=['boeing-737-200-high-density'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='boeing-737-200-high-density',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Passagiere',
    engine_type='turbine',
    intro_year=1968,
    intro_month=2,
    retire_year=1988,
    retire_month=8,
    speed=778,
    weight=27.4,
    power=25560,
    tractive_effort=142,
    payload=115,
    min_loading_time=2400,
    max_loading_time=2400,
    catering_level=2,
    cost=40000000,
    runningcost=154,
    fixed_cost=77778,
    sound='laxspotter97-boeing737-200.wav',
    minimum_runway_length=2189,
    range=3520,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 115],
    comfort_by_class=[0, 0, 105],
    upgrade=['boeing-737-200'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
