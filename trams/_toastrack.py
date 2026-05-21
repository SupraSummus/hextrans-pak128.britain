"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Toastrack',
    waytype='tram_track',
    copyright='James',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1890,
    intro_month=4,
    retire_year=1900,
    retire_month=3,
    speed=32,
    length=4,
    weight=7.5,
    axles=4,
    power=23,
    gear=80,
    tractive_effort=26,
    payload=40,
    min_loading_time=12,
    max_loading_time=45,
    overcrowded_capacity=0,
    comfort=22,
    cost=170000,
    runningcost=14,
    fixed_cost=6142,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Blackpool-red', 'Blackpool-green'],
    way_constraint_permissive=[1],
    blend='trams/toastrack-red.blend',
    upstream_dat='trams/toastrack.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
