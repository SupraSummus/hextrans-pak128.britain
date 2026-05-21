"""merryweather-standard-2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Gladwin (vol. 3) p. 23 (and p. 24 for illustrations)
SPEC = Vehicle(
    name='merryweather-standard-2',
    waytype='tram_track',
    copyright='jamespetts',
    engine_type='steam',
    intro_year=1879,
    intro_month=12,
    retire_year=1890,
    retire_month=5,
    speed=14,
    length=3,
    weight=5.0,
    axles=2,
    power=3,
    tractive_effort=8,
    cost=201000,
    runningcost=3,
    fixed_cost=16168,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='laurie-barclay-0-4-0.wav',
    constraint_prev=['none'],
    blend='trams/merryweather-standard-2.blend',
    upstream_dat='trams/merryweather-standard-2.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
