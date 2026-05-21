"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Bulk16T',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='Kohle',
    intro_year=1921,
    intro_month=5,
    retire_year=1969,
    retire_month=4,
    speed=56,
    length=3,
    weight=7,
    axle_load=12,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=28750,
    payload=16,
    min_loading_time=480,
    max_loading_time=600,
    cost=160000,
    runningcost=0,
    fixed_cost=133,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/bulk-16t.blend',
    upstream_dat='trains/wagon-bulk-16t.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
