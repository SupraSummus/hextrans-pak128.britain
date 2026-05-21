"""1-deck-trailer."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='1-Deck-Trailer',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    intro_year=1860,
    intro_month=8,
    retire_year=1895,
    retire_month=10,
    speed=16,
    length=2,
    weight=2.2,
    axles=2,
    payload=18,
    min_loading_time=12,
    max_loading_time=30,
    overcrowded_capacity=4,
    comfort=38,
    cost=100000,
    runningcost=0,
    fixed_cost=6119,
    years_before_maintenance_max_reached=75,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['tram-horse-irish-draught-single', 'tram-horse-irish-draught-double', 'tram-horse-shire-single', 'tram-horse-shire-double', 'tram-horse-clydesdale-single', 'tram-horse-clydesdale-double', 'kitson-standard-1', 'kitson-standard-2', 'kitson-standard-3', 'wilkinson-engine', 'merryweather-standard-1', 'merryweather-standard-2'],
    constraint_next=['none'],
    blend='trams/1-deck-trailer.blend',
    upstream_dat='trams/1-deck-trailer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
