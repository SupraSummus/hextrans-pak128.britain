"""large-2-deck-trailer."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# 7 window Starbuck/Milnes type - see Gladwin (vol. 3) p. 40
SPEC = Vehicle(
    name='Large-2-Deck-Trailer',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    intro_year=1883,
    intro_month=4,
    retire_year=1902,
    retire_month=3,
    speed=16,
    length=6,
    weight=3.9,
    axles=4,
    payload=62,
    min_loading_time=10,
    max_loading_time=60,
    overcrowded_capacity=7,
    comfort=37,
    cost=375000,
    runningcost=0,
    fixed_cost=6446,
    years_before_maintenance_max_reached=65,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['tram-horse-irish-draught-double', 'tram-horse-shire-double', 'tram-horse-clydesdale-double', 'kitson-standard-1', 'kitson-standard-2', 'kitson-standard-3', 'wilkinson-engine', 'merryweather-standard-1', 'merryweather-standard-2'],
    constraint_next=['none'],
    blend='trams/medium-large-2-deck-trailer.blend',
    upstream_dat='trams/large-2-deck-trailer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
