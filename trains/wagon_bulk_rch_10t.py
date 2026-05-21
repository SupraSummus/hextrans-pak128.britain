"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BulkRCH10T',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='Kohle',
    intro_year=1883,
    intro_month=5,
    retire_year=1923,
    retire_month=6,
    speed=56,
    length=3,
    weight=7,
    axle_load=8,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=21250,
    payload=10,
    min_loading_time=480,
    max_loading_time=600,
    cost=120000,
    runningcost=0,
    fixed_cost=100,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/bulk-rch-10t.blend',
    upstream_dat='trains/wagon-bulk-rch-10t.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
