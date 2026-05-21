"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='erj-145',
    waytype='air',
    copyright='Emmanuel Baranger',
    freight='Passagiere',
    engine_type='turbine',
    intro_year=1997,
    intro_month=4,
    speed=833,
    weight=12.1,
    power=11340,
    tractive_effort=63,
    payload=50,
    min_loading_time=2320,
    max_loading_time=2320,
    catering_level=1,
    comfort=95,
    cost=30000000,
    runningcost=45,
    fixed_cost=70833,
    sound='bigpickle51-jet-takeoff.wav',
    minimum_runway_length=1380,
    range=2445,
    constraint_prev=['none'],
    constraint_next=['none'],
    blend='air/erj-145.blend',
    upstream_dat='air/erj-145.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
