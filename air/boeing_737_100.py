"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'air/boeing-737-100.blend'
_UPSTREAM_DAT = 'air/boeing-737-100.dat'

SPECS = [
Vehicle(
    name='boeing-737-100',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Passagiere',
    engine_type='turbine',
    intro_year=1967,
    intro_month=12,
    retire_year=1985,
    retire_month=1,
    speed=778,
    weight=25.8,
    power=22320,
    tractive_effort=124,
    payload=73,
    min_loading_time=2400,
    max_loading_time=2400,
    catering_level=2,
    cost=3800000,
    runningcost=134,
    fixed_cost=52639,
    upgrade_price=5000,
    sound='laxspotter97-boeing737-200.wav',
    minimum_runway_length=2012,
    range=2855,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 73, 0, 12],
    comfort_by_class=[0, 0, 105, 0, 170],
    upgrade=['boeing-737-100-high-density'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='boeing-737-100-high-density',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Passagiere',
    engine_type='turbine',
    intro_year=1967,
    intro_month=12,
    retire_year=1985,
    retire_month=1,
    speed=778,
    weight=25.8,
    power=22320,
    tractive_effort=124,
    payload=100,
    min_loading_time=2400,
    max_loading_time=2400,
    catering_level=2,
    cost=3800000,
    runningcost=134,
    fixed_cost=52639,
    upgrade_price=5000,
    sound='laxspotter97-boeing737-200.wav',
    minimum_runway_length=2012,
    range=2855,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 100],
    comfort_by_class=[0, 0, 105],
    upgrade=['boeing-737-100'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
