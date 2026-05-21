"""blackpool-coronation."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-Coronation',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1953,
    intro_month=6,
    retire_year=1958,
    retire_month=5,
    speed=70,
    weight=12,
    axles=4,
    power=134,
    gear=80,
    tractive_effort=50,
    payload=56,
    min_loading_time=10,
    max_loading_time=45,
    overcrowded_capacity=10,
    comfort=48,
    cost=560000,
    runningcost=27,
    fixed_cost=6467,
    increase_maintenance_after_years=5,
    years_before_maintenance_max_reached=12,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    way_constraint_permissive=[1],
    blend='trams/blackpool-coronation.blend',
    upstream_dat='trams/blackpool-coronation.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
