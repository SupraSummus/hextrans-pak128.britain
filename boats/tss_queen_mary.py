"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='TSSQueenMary',
    waytype='water',
    copyright='jamespetts',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1933,
    intro_month=9,
    retire_year=1960,
    retire_month=6,
    speed=39,
    length=12,
    weight=600,
    power=1984,
    payload=1419,
    min_loading_time=1200,
    max_loading_time=1400,
    catering_level=4,
    cost=77000000,
    runningcost=164,
    fixed_cost=632083,
    smoke='Steam',
    sound='ship-horn_a.wav',
    range=140,
    constraint_prev=['none'],
    constraint_next=['TSSQueenMaryMail'],
    payload_by_class=[0, 1419, 0, 720],
    comfort_by_class=[0, 93, 0, 146],
    blend='boats/tss-queen-mary.blend',
    upstream_dat='boats/tss-queen-mary.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
