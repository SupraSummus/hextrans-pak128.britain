"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='dhc3-otter',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Post',
    engine_type='petrol',
    intro_year=1953,
    intro_month=6,
    retire_year=1967,
    retire_month=11,
    speed=195,
    weight=2.0,
    power=448,
    tractive_effort=3,
    payload=1900,
    min_loading_time=1600,
    max_loading_time=1850,
    cost=2000000,
    runningcost=18,
    fixed_cost=51389,
    sound='planelow.wav',
    minimum_runway_length=609,
    range=1520,
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 1900],
    blend='air/dhc3-otter.blend',
    upstream_dat='air/dhc3-otter.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
