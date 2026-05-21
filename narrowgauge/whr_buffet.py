"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='WHR-buffet',
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
    payload=18,
    min_loading_time=25,
    max_loading_time=65,
    catering_level=1,
    cost=599750,
    runningcost=0,
    fixed_cost=18250,
    upgrade_price=40000,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    payload_by_class=[0, 18, 0, 15],
    comfort_by_class=[0, 40, 40, 68],
    liverytype=['FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Green-Cream', 'FR-Cherry-Red', 'FR-Red-Cream'],
    blend='narrowgauge/whr-buffet-nwng.blend',
    upstream_dat='narrowgauge/whr-buffet.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
