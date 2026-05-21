"""blackpool-progress-twin-power."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-ProgressTwin-Power',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1958,
    intro_month=3,
    retire_year=1979,
    retire_month=6,
    speed=70,
    length=6,
    weight=13,
    axles=4,
    power=85,
    gear=80,
    tractive_effort=40,
    payload=53,
    min_loading_time=12,
    max_loading_time=45,
    overcrowded_capacity=6,
    comfort=46,
    cost=352000,
    runningcost=17,
    fixed_cost=6293,
    upgrade_price=12500,
    increase_maintenance_after_years=30,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['Blackpool-ProgressTwin-Trailer', 'none'],
    way_constraint_permissive=[1],
    blend='trams/blackpool-progress-twin-power.blend',
    upstream_dat='trams/blackpool-progress-twin-power.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
