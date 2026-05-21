"""blackpool-millenium."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-Millenium',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1998,
    intro_month=2,
    retire_year=2005,
    retire_month=12,
    speed=70,
    weight=18,
    axles=4,
    power=85,
    gear=80,
    tractive_effort=40,
    payload=94,
    min_loading_time=10,
    max_loading_time=70,
    overcrowded_capacity=6,
    comfort=45,
    cost=700000,
    runningcost=17,
    fixed_cost=6583,
    upgrade_price=19000,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    way_constraint_permissive=[1],
    blend='trams/blackpool-millenium.blend',
    upstream_dat='trams/blackpool-millenium.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
