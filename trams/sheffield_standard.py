"""sheffield-standard."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='sheffield-standard',
    waytype='tram_track',
    copyright='James/jamespetts',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1927,
    intro_month=6,
    retire_year=1939,
    retire_month=9,
    speed=32,
    weight=15.5,
    axles=4,
    power=75,
    gear=80,
    tractive_effort=35,
    payload=61,
    min_loading_time=10,
    max_loading_time=60,
    overcrowded_capacity=6,
    comfort=40,
    cost=416000,
    runningcost=30,
    fixed_cost=6347,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['sheffield-dark', 'sheffield-light'],
    way_constraint_permissive=[1],
    blend='trams/sheffield-standard-dark.blend',
    upstream_dat='trams/sheffield-standard.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
