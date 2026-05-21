"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='WHR-brake',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Passagiere',
    intro_year=1893,
    intro_month=9,
    retire_year=1964,
    retire_month=5,
    speed=60,
    length=5,
    weight=7,
    axles=4,
    rolling_resistance=18,
    payload=28,
    min_loading_time=25,
    max_loading_time=65,
    cost=575000,
    runningcost=0,
    fixed_cost=5040,
    bidirectional=1,
    can_lead_from_rear=0,
    payload_by_class=[0, 28, 0, 0],
    comfort_by_class=[0, 40, 40, 83],
    liverytype=['FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Green-Cream', 'FR-Cherry-Red', 'FR-Red-Cream'],
    blend='narrowgauge/whr-brake-nwng.blend',
    upstream_dat='narrowgauge/whr-brake.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
