"""blackpool-jubilee."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-Jubilee',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1979,
    intro_month=4,
    retire_year=1993,
    retire_month=9,
    speed=70,
    weight=18,
    axles=4,
    power=85,
    gear=80,
    tractive_effort=40,
    payload=94,
    min_loading_time=10,
    max_loading_time=50,
    overcrowded_capacity=6,
    comfort=45,
    cost=656000,
    runningcost=8,
    fixed_cost=6547,
    upgrade_price=15000,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    upgrade=['Blackpool-Millenium'],
    way_constraint_permissive=[1],
    blend='trams/blackpool-jubilee.blend',
    upstream_dat='trams/blackpool-jubilee.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
