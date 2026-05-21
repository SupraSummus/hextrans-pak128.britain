"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'narrowgauge/fr-bogie-van-royal-purple.blend'
_UPSTREAM_DAT = 'narrowgauge/fr-bogie-van.dat'

SPECS = [
Vehicle(
    name='FR-bogie-van-unfitted',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Post',
    intro_year=1872,
    intro_month=12,
    retire_year=1886,
    retire_month=10,
    speed=60,
    length=3,
    weight=4,
    axles=4,
    brake_force=1,
    rolling_resistance=19,
    payload=150,
    min_loading_time=35,
    max_loading_time=75,
    cost=370000,
    runningcost=0,
    fixed_cost=4954,
    bidirectional=1,
    can_lead_from_rear=0,
    liverytype=['FR-Royal-Purple', 'FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Green-Cream', 'FR-Cherry-Red', 'FR-Red-Cream'],
    upgrade=['FR-bogie-van-fitted'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='FR-bogie-van-fitted',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Post',
    intro_year=1886,
    intro_month=10,
    retire_year=1964,
    retire_month=5,
    speed=60,
    length=3,
    weight=4,
    rolling_resistance=19,
    payload=150,
    min_loading_time=35,
    max_loading_time=75,
    cost=370000,
    runningcost=0,
    fixed_cost=440,
    upgrade_price=24000,
    bidirectional=1,
    can_lead_from_rear=0,
    liverytype=['FR-Royal-Purple', 'FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Green-Cream', 'FR-Cherry-Red', 'FR-Red-Cream'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
