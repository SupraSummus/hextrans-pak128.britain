"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='2-Deck-Open',
    waytype='tram_track',
    copyright='James/jamespetts',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1899,
    intro_month=10,
    retire_year=1920,
    retire_month=2,
    speed=32,
    length=5,
    weight=10,
    axles=2,
    power=37,
    gear=80,
    tractive_effort=27,
    payload=51,
    min_loading_time=10,
    max_loading_time=45,
    overcrowded_capacity=5,
    comfort=33,
    cost=360000,
    runningcost=22,
    fixed_cost=6300,
    upgrade_price=175000,
    bidirectional=1,
    can_lead_from_rear=1,
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Sheffield-dark', 'Sheffield-light', 'Glasgow-Corporation-early'],
    way_constraint_permissive=[1],
    blend='trams/2-deck-open.blend',
    upstream_dat='trams/2-deck-open.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
