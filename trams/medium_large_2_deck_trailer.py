"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Medium-large-2-Deck-Trailer',
    waytype='tram_track',
    copyright='James/jamespetts',
    freight='Passagiere',
    intro_year=1877,
    intro_month=3,
    retire_year=1889,
    retire_month=2,
    speed=16,
    length=5,
    weight=3.0,
    axles=4,
    payload=54,
    min_loading_time=10,
    max_loading_time=57,
    overcrowded_capacity=6,
    comfort=34,
    cost=300000,
    runningcost=0,
    fixed_cost=6357,
    years_before_maintenance_max_reached=72,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['tram-horse-irish-draught-double', 'tram-horse-shire-double', 'tram-horse-clydesdale-double', 'kitson-standard-1', 'kitson-standard-2', 'kitson-standard-3', 'wilkinson-engine', 'merryweather-standard-1', 'merryweather-standard-2'],
    constraint_next=['none'],
    upgrade=['2-Deck-Open'],
    blend='trams/medium-large-2-deck-trailer.blend',
    upstream_dat='trams/medium-large-2-deck-trailer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
