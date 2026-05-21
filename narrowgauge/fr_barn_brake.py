"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='FR-Barn-Brake',
    waytype='narrowgauge_track',
    copyright='James',
    freight='Passagiere',
    intro_year=1964,
    intro_month=5,
    retire_year=1997,
    retire_month=6,
    speed=80,
    length=6,
    weight=8,
    axles=4,
    rolling_resistance=17,
    payload=24,
    min_loading_time=20,
    max_loading_time=60,
    cost=570000,
    runningcost=0,
    fixed_cost=5038,
    bidirectional=1,
    can_lead_from_rear=0,
    payload_by_class=[0, 24, 0, 0],
    comfort_by_class=[0, 65, 65, 85],
    liverytype=['FR-Green-Cream', 'FR-Cherry-Red', 'FR-Red-Cream'],
    blend='narrowgauge/fr-barn-red-cream.blend',
    upstream_dat='narrowgauge/fr-barn-brake.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
