"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-Original',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1885,
    intro_month=9,
    retire_year=1894,
    retire_month=10,
    speed=30,
    length=3,
    weight=7,
    axles=2,
    power=22,
    gear=80,
    tractive_effort=24,
    payload=55,
    min_loading_time=10,
    max_loading_time=50,
    overcrowded_capacity=4,
    comfort=33,
    cost=220000,
    runningcost=13,
    fixed_cost=6183,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    way_constraint_permissive=[1],
    blend='trams/blackpool-original.blend',
    upstream_dat='trams/blackpool-original.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
