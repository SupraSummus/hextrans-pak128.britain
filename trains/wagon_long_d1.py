"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LongD1',
    waytype='track',
    copyright='James',
    freight='Bretter',
    intro_year=1855,
    intro_month=1,
    retire_year=1903,
    retire_month=5,
    speed=56,
    length=3,
    weight=4.3,
    axle_load=6,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=15000,
    payload=8,
    min_loading_time=360,
    max_loading_time=975,
    cost=100000,
    runningcost=0,
    fixed_cost=83,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/long-d1.blend',
    upstream_dat='trains/wagon-long-d1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
