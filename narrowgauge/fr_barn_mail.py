"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='FR-Barn-Mail',
    waytype='narrowgauge_track',
    copyright='James',
    freight='Post',
    intro_year=1964,
    intro_month=5,
    speed=80,
    length=6,
    weight=8,
    axles=4,
    rolling_resistance=17,
    payload=200,
    min_loading_time=30,
    max_loading_time=150,
    cost=570000,
    runningcost=0,
    fixed_cost=238,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    liverytype=['FR-Green-Cream', 'FR-Cherry-Red', 'FR-Red-Cream'],
    blend='narrowgauge/fr-barn-red-cream.blend',
    upstream_dat='narrowgauge/fr-barn-mail.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
