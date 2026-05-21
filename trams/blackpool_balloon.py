"""blackpool-balloon."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-Balloon',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1934,
    intro_month=12,
    retire_year=1957,
    retire_month=5,
    speed=65,
    weight=17.5,
    axles=4,
    power=85,
    gear=80,
    tractive_effort=40,
    payload=78,
    min_loading_time=12,
    max_loading_time=67,
    overcrowded_capacity=8,
    comfort=49,
    cost=600000,
    runningcost=34,
    fixed_cost=6500,
    increase_maintenance_after_years=30,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Blackpool-green', 'WW2-Austerity', 'Blackpool-green-postwar', 'Blackpool-purple'],
    upgrade=['Blackpool-Jubilee', 'Blackpool-Millenium'],
    way_constraint_permissive=[1],
    blend='trams/blackpool-balloon-austerity.blend',
    upstream_dat='trams/blackpool-balloon.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
