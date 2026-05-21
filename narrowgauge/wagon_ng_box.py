"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='wagon-ng-box',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Bucher',
    intro_year=1836,
    intro_month=5,
    retire_year=1948,
    retire_month=9,
    speed=50,
    length=2,
    weight=1,
    axle_load=1,
    brake_force=0,
    rolling_resistance=20,
    way_wear_factor=4400,
    payload=3,
    min_loading_time=200,
    max_loading_time=600,
    cost=38000,
    runningcost=0,
    fixed_cost=16,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='narrowgauge/ng-box.blend',
    upstream_dat='narrowgauge/wagon-ng-box.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
