"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Bulk8T',
    waytype='track',
    copyright='Kieron',
    freight='Kohle',
    intro_year=1855,
    intro_month=2,
    retire_year=1903,
    retire_month=8,
    speed=56,
    length=3,
    weight=4,
    axle_load=6,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=15000,
    payload=8,
    min_loading_time=480,
    max_loading_time=600,
    cost=100000,
    runningcost=0,
    fixed_cost=83,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/bulk-8t.blend',
    upstream_dat='trains/wagon-bulk-8t.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
