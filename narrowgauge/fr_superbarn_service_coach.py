"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='FR-Superbarn-service-coach',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Passagiere',
    intro_year=1997,
    intro_month=6,
    speed=80,
    length=6,
    weight=11,
    axles=4,
    rolling_resistance=17,
    payload=0,
    min_loading_time=20,
    max_loading_time=60,
    catering_level=2,
    cost=786000,
    runningcost=0,
    fixed_cost=1638,
    bidirectional=1,
    can_lead_from_rear=0,
    blend='narrowgauge/fr-superbarn-service-coach-red-cream.blend',
    upstream_dat='narrowgauge/fr-superbarn-service-coach.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
