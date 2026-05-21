"""blackpool-progress-twin-trailer."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Blackpool-ProgressTwin-Trailer',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    intro_year=1958,
    intro_month=3,
    retire_year=1979,
    retire_month=6,
    speed=70,
    weight=9,
    axles=4,
    payload=53,
    min_loading_time=12,
    max_loading_time=45,
    overcrowded_capacity=6,
    comfort=46,
    cost=202000,
    runningcost=0,
    fixed_cost=6240,
    increase_maintenance_after_years=30,
    bidirectional=1,
    can_lead_from_rear=1,
    constraint_prev=['Blackpool-ProgressTwin-Power'],
    constraint_next=['none'],
    blend='trams/blackpool-progress-twin-trailer.blend',
    upstream_dat='trams/blackpool-progress-twin-trailer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
