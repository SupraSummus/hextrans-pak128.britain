"""glasgow-coronation."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.semple.biz/glasgow/tram%20rolling%20stock.shtml
# Dimensions not available, so guessed based on similar types
SPEC = Vehicle(
    name='glasgow-coronation',
    waytype='tram_track',
    copyright='James&JamesPetts',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1937,
    intro_month=6,
    retire_year=1949,
    retire_month=3,
    speed=67,
    weight=17.8,
    axles=4,
    power=104,
    gear=80,
    tractive_effort=34,
    payload=64,
    min_loading_time=10,
    max_loading_time=54,
    overcrowded_capacity=10,
    comfort=53,
    cost=500000,
    runningcost=42,
    fixed_cost=6417,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Glasgow-Corporation-standard'],
    way_constraint_permissive=[1],
    blend='trams/glasgow-coronation.blend',
    upstream_dat='trams/glasgow-coronation.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
