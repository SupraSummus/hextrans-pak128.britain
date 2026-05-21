"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MVBalmoral',
    waytype='water',
    copyright='Zeno/jamespetts',
    freight='Passagiere',
    engine_type='diesel',
    intro_year=1949,
    intro_month=3,
    retire_year=1968,
    retire_month=12,
    speed=35,
    length=12,
    weight=300,
    power=700,
    payload=500,
    min_loading_time=1200,
    max_loading_time=1400,
    catering_level=3,
    cost=80000000,
    runningcost=145,
    fixed_cost=233333,
    smoke='Diesel',
    sound='ship-horn_b.wav',
    range=120,
    constraint_prev=['none'],
    constraint_next=['ferry-mail', 'none'],
    payload_by_class=[0, 500, 0, 150],
    comfort_by_class=[0, 110, 0, 127],
    blend='boats/mv-balmoral.blend',
    upstream_dat='boats/mv-balmoral.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
