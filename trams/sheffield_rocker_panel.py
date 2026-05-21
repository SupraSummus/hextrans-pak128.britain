"""sheffield-rocker-panel."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='sheffield-rocker-panel',
    waytype='tram_track',
    copyright='James/jamespetts',
    freight='Passagiere',
    engine_type='electric',
    intro_year=1918,
    intro_month=12,
    retire_year=1929,
    retire_month=9,
    speed=32,
    weight=15.7,
    axles=2,
    power=60,
    gear=80,
    tractive_effort=36,
    payload=76,
    min_loading_time=10,
    max_loading_time=66,
    overcrowded_capacity=6,
    comfort=35,
    cost=397500,
    runningcost=36,
    fixed_cost=6331,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='tom-tait-tram.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['Sheffield-dark', 'Sheffield-light'],
    way_constraint_permissive=[1],
    blend='trams/sheffield-rocker-panel-dark.blend',
    upstream_dat='trams/sheffield-rocker-panel.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
