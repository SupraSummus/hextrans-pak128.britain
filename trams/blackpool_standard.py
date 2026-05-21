"""blackpool-standard."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-Standard',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1923,
    intro_month=8,
    retire_year=1936,
    retire_month=1,
    speed=32,
    weight=17.5,
    axles=4,
    power=60,
    gear=80,
    tractive_effort=35,
    payload=78,
    min_loading_time=10,
    max_loading_time=67,
    overcrowded_capacity=6,
    comfort=37,
    cost=415000,
    runningcost=24,
    fixed_cost=6346,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Blackpool-red', 'Blackpool-green', 'WW2-Austerity'],
    way_constraint_permissive=[1],
    blend='trams/blackpool-standard-austerity.blend',
    upstream_dat='trams/blackpool-standard.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
