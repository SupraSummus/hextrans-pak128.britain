"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='ClydeSteamer',
    waytype='water',
    copyright='Druid/James',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1860,
    intro_month=2,
    retire_year=1886,
    retire_month=1,
    speed=26,
    length=12,
    weight=320,
    power=1000,
    payload=300,
    min_loading_time=1200,
    max_loading_time=1400,
    cost=44928000,
    runningcost=51,
    fixed_cost=218720,
    smoke='Steam',
    sound='ship-horn_b.wav',
    range=150,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 300, 0, 150],
    comfort_by_class=[0, 38, 0, 80],
    blend='boats/clyde-steamer.blend',
    upstream_dat='boats/clyde-steamer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
