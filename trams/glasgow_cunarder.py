"""glasgow-cunarder."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.semple.biz/glasgow/tram%20rolling%20stock.shtml
# Dimensions not available, so guessed based on similar types
SPEC = Vehicle(
    name='glasgow-cunarder',
    waytype='tram_track',
    copyright='James&JamesPetts',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1948,
    intro_month=7,
    retire_year=1954,
    retire_month=5,
    speed=67,
    weight=17.5,
    axles=4,
    power=107,
    gear=80,
    tractive_effort=33,
    payload=70,
    min_loading_time=10,
    max_loading_time=54,
    overcrowded_capacity=10,
    comfort=53,
    cost=510000,
    runningcost=21,
    fixed_cost=6425,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Glasgow-Corporation-standard'],
    way_constraint_permissive=[1],
    blend='trams/glasgow-cunarder.blend',
    upstream_dat='trams/glasgow-cunarder.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
