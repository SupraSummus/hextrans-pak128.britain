"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='IronPaddleSteamer',
    waytype='water',
    copyright='James',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1844,
    intro_month=2,
    retire_year=1873,
    retire_month=6,
    speed=22,
    length=8,
    weight=45,
    power=90,
    payload=200,
    min_loading_time=2400,
    max_loading_time=2700,
    cost=15676416,
    runningcost=18,
    fixed_cost=206532,
    smoke='Steam',
    sound='ship-horn_b.wav',
    range=100,
    constraint_prev=['none'],
    constraint_next=['IronPaddleSteamerMail'],
    payload_by_class=[0, 200, 0, 120],
    comfort_by_class=[0, 36, 0, 68],
    blend='boats/iron-paddle-steamer.blend',
    upstream_dat='boats/iron-paddle-steamer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
