"""lut-type-t."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See "London Tramways" (John Reed, pub. Capital Transport, ISBN 1-85414-179-1) p. 67
SPEC = Vehicle(
    name='lut-type-t',
    waytype='tram_track',
    copyright='James/jamespetts',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1906,
    intro_month=3,
    retire_year=1931,
    retire_month=11,
    speed=32,
    length=5,
    weight=14.6,
    axles=4,
    power=45,
    gear=80,
    tractive_effort=33,
    payload=74,
    min_loading_time=10,
    max_loading_time=65,
    overcrowded_capacity=7,
    comfort=40,
    cost=457500,
    runningcost=27,
    fixed_cost=6381,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['LUT-vermillion', 'LT'],
    way_constraint_permissive=[1],
    blend='trams/lut-type-t-lt.blend',
    upstream_dat='trams/lut-type-t.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
