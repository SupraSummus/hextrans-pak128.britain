"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='sheffield-preston',
    waytype='tram_track',
    copyright='James/jamespetts',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1907,
    intro_month=8,
    retire_year=1919,
    retire_month=5,
    speed=32,
    weight=12,
    axles=2,
    power=52,
    gear=80,
    tractive_effort=35,
    payload=58,
    min_loading_time=10,
    max_loading_time=60,
    overcrowded_capacity=5,
    comfort=34,
    cost=375000,
    runningcost=31,
    fixed_cost=6313,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Sheffield-dark', 'Sheffield-light'],
    way_constraint_permissive=[1],
    blend='trams/sheffield-preston-dark.blend',
    upstream_dat='trams/sheffield-preston.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
