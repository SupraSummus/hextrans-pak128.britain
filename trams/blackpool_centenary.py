"""blackpool-centenary."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-Centenary',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1984,
    intro_month=1,
    retire_year=2015,
    retire_month=1,
    speed=70,
    weight=17.5,
    axles=4,
    power=85,
    gear=80,
    tractive_effort=40,
    payload=52,
    min_loading_time=15,
    max_loading_time=40,
    overcrowded_capacity=16,
    comfort=45,
    cost=434000,
    runningcost=8,
    fixed_cost=6362,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    way_constraint_permissive=[1],
    blend='trams/blackpool-centenary.blend',
    upstream_dat='trams/blackpool-centenary.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
