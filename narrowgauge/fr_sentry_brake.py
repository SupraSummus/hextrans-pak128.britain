"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='fr-sentry-brake',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Post',
    intro_year=1863,
    intro_month=7,
    retire_year=1873,
    retire_month=4,
    speed=60,
    length=2,
    weight=1.4,
    axles=2,
    brake_force=1,
    rolling_resistance=20,
    payload=60,
    min_loading_time=25,
    max_loading_time=50,
    cost=262000,
    runningcost=0,
    fixed_cost=4863,
    bidirectional=1,
    can_lead_from_rear=0,
    blend='narrowgauge/fr-sentry-brake.blend',
    upstream_dat='narrowgauge/fr-sentry-brake.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
