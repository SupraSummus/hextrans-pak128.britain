"""blackpool-ee-railcoach."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-EE-Railcoach',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1934,
    intro_month=3,
    retire_year=1938,
    retire_month=9,
    speed=65,
    weight=11.4,
    axles=4,
    power=85,
    gear=80,
    tractive_effort=40,
    payload=48,
    min_loading_time=10,
    max_loading_time=55,
    overcrowded_capacity=6,
    comfort=49,
    cost=410000,
    runningcost=34,
    fixed_cost=6342,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Blackpool-green', 'WW2-Austerity', 'Blackpool-green-postwar'],
    upgrade=['Blackpool-ProgressTwin-Power'],
    way_constraint_permissive=[1],
    blend='trams/blackpool-ee-railcoach-austerity.blend',
    upstream_dat='trams/blackpool-ee-railcoach.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
