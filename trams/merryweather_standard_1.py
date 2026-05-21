"""merryweather-standard-1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Gladwin (vol. 1) p. 79
SPEC = Vehicle(
    name='merryweather-standard-1',
    waytype='tram_track',
    copyright='jamespetts',
    engine_type='steam',
    intro_year=1875,
    intro_month=9,
    retire_year=1880,
    retire_month=2,
    speed=12,
    length=2,
    weight=4.0,
    axles=2,
    power=2,
    tractive_effort=6,
    cost=178000,
    runningcost=2,
    fixed_cost=16148,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='laurie-barclay-0-4-0.wav',
    constraint_prev=['none'],
    blend='trams/merryweather-standard-1.blend',
    upstream_dat='trams/merryweather-standard-1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
