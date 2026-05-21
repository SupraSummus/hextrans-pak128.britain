"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='lut-type-z',
    waytype='tram_track',
    copyright='James/jamespetts',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1901,
    intro_month=6,
    retire_year=1906,
    retire_month=7,
    speed=32,
    length=5,
    weight=13,
    axles=4,
    power=37,
    gear=80,
    tractive_effort=30,
    payload=69,
    min_loading_time=10,
    max_loading_time=61,
    overcrowded_capacity=6,
    comfort=37,
    cost=425000,
    runningcost=22,
    fixed_cost=6354,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['LUT-vermillion', 'LT'],
    way_constraint_permissive=[1],
    blend='trams/lut-type-z.blend',
    upstream_dat='trams/lut-type-z.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
