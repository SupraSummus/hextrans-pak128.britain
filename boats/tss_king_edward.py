"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='TSSKingEdward',
    waytype='water',
    copyright='jamespetts',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1901,
    intro_month=5,
    retire_year=1933,
    retire_month=9,
    speed=38,
    length=12,
    weight=550,
    power=1827,
    payload=1286,
    min_loading_time=1200,
    max_loading_time=1400,
    catering_level=4,
    cost=74000000,
    runningcost=114,
    fixed_cost=630833,
    smoke='Steam',
    sound='ship-horn_a.wav',
    range=120,
    constraint_prev=['none'],
    constraint_next=['TSSKingEdwardMail'],
    payload_by_class=[0, 1286, 0, 650],
    comfort_by_class=[0, 91, 0, 142],
    blend='boats/tss-king-edward.blend',
    upstream_dat='boats/tss-king-edward.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
