"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'air/dh-comet-4c.blend'
_UPSTREAM_DAT = 'air/dh-comet-4c.dat'

SPECS = [
Vehicle(
    name='dh-comet-4c',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Passagiere',
    engine_type='turbine',
    intro_year=1960,
    intro_month=1,
    retire_year=1966,
    retire_month=10,
    speed=805,
    weight=36.1,
    power=28195,
    tractive_effort=187,
    payload=51,
    min_loading_time=2400,
    max_loading_time=2400,
    catering_level=4,
    cost=14400000,
    runningcost=170,
    fixed_cost=60000,
    upgrade_price=5000,
    sound='robin-pinnock-bac-1-11.wav',
    minimum_runway_length=2290,
    range=6900,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 51, 0, 28],
    comfort_by_class=[0, 0, 124, 0, 151],
    upgrade=['dh-comet-4c-high-density'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='dh-comet-4c-high-density',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Passagiere',
    engine_type='turbine',
    intro_year=1960,
    intro_month=1,
    retire_year=1966,
    retire_month=10,
    speed=805,
    weight=36.1,
    power=28195,
    tractive_effort=187,
    payload=119,
    min_loading_time=2400,
    max_loading_time=2400,
    catering_level=4,
    cost=14400000,
    runningcost=170,
    fixed_cost=60000,
    upgrade_price=5000,
    sound='robin-pinnock-bac-1-11.wav',
    minimum_runway_length=2290,
    range=6900,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 119],
    comfort_by_class=[0, 0, 124],
    upgrade=['dh-comet-4c'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
