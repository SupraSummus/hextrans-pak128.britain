"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'narrowgauge/fr-bogie-royal-purple.blend'
_UPSTREAM_DAT = 'narrowgauge/fr-bogie.dat'

SPECS = [
Vehicle(
    name='FR-bogie-unfitted',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Passagiere',
    intro_year=1872,
    intro_month=12,
    retire_year=1886,
    retire_month=10,
    speed=60,
    length=5,
    weight=6.1,
    axles=4,
    brake_force=0,
    rolling_resistance=19,
    payload=32,
    min_loading_time=17,
    max_loading_time=47,
    cost=520000,
    runningcost=0,
    fixed_cost=619,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    payload_by_class=[0, 32, 16, 6],
    comfort_by_class=[0, 37, 40, 83],
    liverytype=['FR-Royal-Purple', 'FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Green-Cream', 'FR-Cherry-Red', 'FR-Red-Cream'],
    upgrade=['FR-bogie-fitted'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='FR-bogie-fitted',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Passagiere',
    intro_year=1886,
    intro_month=10,
    retire_year=1893,
    retire_month=6,
    speed=60,
    length=5,
    weight=6.1,
    rolling_resistance=19,
    payload=32,
    min_loading_time=15,
    max_loading_time=55,
    cost=560000,
    runningcost=0,
    fixed_cost=5033,
    upgrade_price=26000,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    payload_by_class=[0, 32, 16, 6],
    comfort_by_class=[0, 37, 40, 83],
    liverytype=['FR-Royal-Purple', 'FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Green-Cream', 'FR-Cherry-Red', 'FR-Red-Cream'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
