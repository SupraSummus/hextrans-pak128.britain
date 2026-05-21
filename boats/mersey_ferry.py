"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MerseyFerry',
    waytype='water',
    copyright='James',
    freight='Passagiere',
    engine_type='diesel',
    intro_year=1959,
    intro_month=1,
    speed=26,
    length=12,
    weight=460,
    power=1100,
    payload=860,
    min_loading_time=120,
    max_loading_time=860,
    cost=56146000,
    runningcost=224,
    fixed_cost=223394,
    smoke='Diesel',
    sound='ship-horn_b.wav',
    range=60,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 860],
    comfort_by_class=[0, 61],
    blend='boats/mersey-ferry.blend',
    upstream_dat='boats/mersey-ferry.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
