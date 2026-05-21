"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='wagon-ng-long',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Bretter',
    intro_year=1836,
    intro_month=5,
    retire_year=1948,
    retire_month=9,
    speed=50,
    length=2,
    weight=1,
    axle_load=2,
    brake_force=0,
    rolling_resistance=20,
    way_wear_factor=3750,
    payload=2,
    min_loading_time=320,
    max_loading_time=400,
    cost=32000,
    runningcost=0,
    fixed_cost=53,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='narrowgauge/ng-long.blend',
    upstream_dat='narrowgauge/wagon-ng-long.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
