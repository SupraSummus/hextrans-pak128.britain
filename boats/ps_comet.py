"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='PSComet',
    waytype='water',
    copyright='James',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1812,
    intro_month=5,
    retire_year=1840,
    retire_month=6,
    speed=15,
    length=8,
    weight=29,
    power=55,
    payload=40,
    min_loading_time=1800,
    max_loading_time=2400,
    cost=8709120,
    runningcost=16,
    fixed_cost=22048,
    smoke='Steam',
    sound='ship-horn_b.wav',
    range=60,
    constraint_prev=['none'],
    constraint_next=['PSCometMail'],
    payload_by_class=[0, 40],
    comfort_by_class=[0, 38],
    blend='boats/comet.blend',
    upstream_dat='boats/ps-comet.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
