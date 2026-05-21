"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-Dreadnought',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1895,
    intro_month=6,
    retire_year=1900,
    retire_month=5,
    speed=32,
    length=4,
    weight=11.7,
    axles=4,
    power=30,
    gear=80,
    tractive_effort=26,
    payload=65,
    min_loading_time=8,
    max_loading_time=65,
    overcrowded_capacity=3,
    comfort=31,
    cost=325000,
    runningcost=18,
    fixed_cost=6271,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Blackpool-red', 'Blackpool-green'],
    way_constraint_permissive=[1],
    blend='trams/blackpool-dreadnought-red.blend',
    upstream_dat='trams/blackpool-dreadnought.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
