"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='FR-Superbarn',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Passagiere',
    intro_year=1997,
    intro_month=6,
    speed=80,
    length=6,
    weight=10,
    axles=4,
    rolling_resistance=17,
    payload=36,
    min_loading_time=20,
    max_loading_time=60,
    cost=745000,
    runningcost=0,
    fixed_cost=1552,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    payload_by_class=[0, 36, 0, 0],
    comfort_by_class=[0, 67, 67, 155],
    blend='narrowgauge/fr-superbarn-red-cream.blend',
    upstream_dat='narrowgauge/fr-superbarn.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
