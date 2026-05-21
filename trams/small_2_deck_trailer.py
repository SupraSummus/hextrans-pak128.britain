"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Small-2-Deck-Trailer',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    intro_year=1874,
    intro_month=3,
    retire_year=1895,
    retire_month=12,
    speed=16,
    length=4,
    weight=1.9,
    axles=2,
    payload=36,
    min_loading_time=10,
    max_loading_time=55,
    overcrowded_capacity=3,
    comfort=32,
    cost=175000,
    runningcost=0,
    fixed_cost=6208,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['tram-horse-irish-draught-single', 'tram-horse-irish-draught-double', 'tram-horse-shire-single', 'tram-horse-shire-double', 'tram-horse-clydesdale-single', 'tram-horse-clydesdale-double', 'kitson-standard-1', 'kitson-standard-2', 'kitson-standard-3', 'wilkinson-engine', 'merryweather-standard-1', 'merryweather-standard-2'],
    constraint_next=['none'],
    blend='trams/small-2-deck-trailer.blend',
    upstream_dat='trams/small-2-deck-trailer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
