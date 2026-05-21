"""wagon-tta."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Air Braked Tanker (TTA)',
    waytype='track',
    copyright='Kieron',
    freight='Oel',
    intro_year=1964,
    intro_month=4,
    retire_year=1980,
    retire_month=9,
    speed=96,
    length=5,
    weight=13,
    axle_load=21,
    way_wear_factor=52500,
    payload=34,
    min_loading_time=480,
    max_loading_time=600,
    cost=200000,
    runningcost=0,
    fixed_cost=167,
    bidirectional=1,
    can_lead_from_rear=0,
    blend='trains/Wagons/tta.blend',
    upstream_dat='trains/wagon-tta.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
