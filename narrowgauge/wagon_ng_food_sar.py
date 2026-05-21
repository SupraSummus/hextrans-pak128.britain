"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='wagon-ng-food-sar',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='meat',
    intro_year=1966,
    intro_month=3,
    speed=60,
    length=5,
    weight=5,
    axle_load=3,
    rolling_resistance=13,
    way_wear_factor=12500,
    payload=10,
    min_loading_time=200,
    max_loading_time=600,
    cost=126350,
    runningcost=0,
    fixed_cost=70,
    bidirectional=1,
    blend='narrowgauge/ng-food-sar.blend',
    upstream_dat='narrowgauge/wagon-ng-food-sar.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
