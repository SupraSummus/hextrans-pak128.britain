"""extra-large-2-deck-trailer."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# 8 window Starbuck/Milnes type - see Gladwin (vol. 3) p. 40
SPEC = Vehicle(
    name='Extra-large-2-Deck-Trailer',
    waytype='tram_track',
    copyright='James/jamespetts',
    freight='Passagiere',
    intro_year=1889,
    intro_month=5,
    retire_year=1907,
    retire_month=7,
    speed=16,
    length=7,
    weight=4.5,
    axles=4,
    payload=74,
    min_loading_time=10,
    max_loading_time=66,
    overcrowded_capacity=8,
    comfort=37,
    cost=410000,
    runningcost=0,
    fixed_cost=6488,
    years_before_maintenance_max_reached=60,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['tram-horse-irish-draught-double', 'tram-horse-shire-double', 'tram-horse-clydesdale-double', 'kitson-standard-1', 'kitson-standard-2', 'kitson-standard-3', 'wilkinson-engine', 'merryweather-standard-1', 'merryweather-standard-2'],
    constraint_next=['none'],
    blend='trams/extra-large-2-deck-trailer.blend',
    upstream_dat='trams/extra-large-2-deck-trailer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
