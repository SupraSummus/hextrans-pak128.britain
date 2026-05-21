"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='WoodenPaddleSteamer',
    waytype='water',
    copyright='James',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1820,
    intro_month=5,
    retire_year=1860,
    retire_month=3,
    speed=15,
    length=8,
    weight=45,
    power=90,
    payload=300,
    min_loading_time=2400,
    max_loading_time=2700,
    cost=13063680,
    runningcost=26,
    fixed_cost=209072,
    smoke='Steam',
    range=100,
    constraint_prev=['none'],
    constraint_next=['WoodenPaddleSteamerMail'],
    payload_by_class=[0, 300],
    comfort_by_class=[0, 33],
    blend='boats/wooden-paddle-steamer.blend',
    upstream_dat='boats/wooden-paddle-steamer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
