"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='TyneFerry',
    waytype='water',
    copyright='jamespetts',
    freight='Passagiere',
    engine_type='diesel',
    intro_year=1940,
    intro_month=2,
    retire_year=1992,
    retire_month=6,
    speed=25,
    length=12,
    weight=50,
    power=100,
    payload=313,
    min_loading_time=60,
    max_loading_time=360,
    cost=32000000,
    runningcost=22,
    fixed_cost=213333,
    smoke='Diesel',
    sound='ship-horn_b.wav',
    range=60,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 313],
    comfort_by_class=[0, 51],
    blend='boats/tyne-ferry.blend',
    upstream_dat='boats/tyne-ferry.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
