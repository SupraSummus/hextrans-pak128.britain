"""glasgow-room-and-kitchen."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.semple.biz/glasgow/tram%20rolling%20stock.shtml
SPEC = Vehicle(
    name='glasgow-room-and-kitchen',
    waytype='tram_track',
    copyright='James/jamespetts',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1898,
    intro_month=3,
    retire_year=1909,
    retire_month=2,
    speed=32,
    length=5,
    weight=8.9,
    axles=4,
    power=52,
    gear=80,
    tractive_effort=32,
    payload=32,
    min_loading_time=15,
    max_loading_time=42,
    overcrowded_capacity=3,
    comfort=35,
    cost=300000,
    runningcost=31,
    fixed_cost=6250,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Glasgow-Corporation-early'],
    way_constraint_permissive=[1],
    blend='trams/glasgow-room-and-kitchen.blend',
    upstream_dat='trams/glasgow-room-and-kitchen.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
