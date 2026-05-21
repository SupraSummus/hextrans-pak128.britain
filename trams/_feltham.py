"""feltham."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See "London Tramways" (John Reed, pub. Capital Transport, ISBN 1-85414-179-1) pp. 80-1
SPEC = Vehicle(
    name='feltham',
    waytype='tram_track',
    copyright='James/jamespetts',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1930,
    intro_month=5,
    retire_year=1943,
    retire_month=7,
    speed=65,
    length=5,
    weight=20,
    axles=4,
    power=104,
    gear=80,
    tractive_effort=38,
    payload=64,
    min_loading_time=9,
    max_loading_time=45,
    overcrowded_capacity=12,
    comfort=49,
    cost=550000,
    runningcost=42,
    fixed_cost=6458,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['LUT-vermillion', 'LT'],
    way_constraint_permissive=[1],
    blend='trams/feltham-lt.blend',
    upstream_dat='trams/feltham.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
