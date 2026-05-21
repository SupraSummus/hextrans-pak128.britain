"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BulkRCH12T',
    waytype='track',
    copyright='Kieron',
    freight='Kohle',
    intro_year=1913,
    intro_month=10,
    retire_year=1943,
    retire_month=11,
    speed=56,
    length=3,
    weight=7.0,
    axle_load=9,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=23750,
    payload=12,
    min_loading_time=480,
    max_loading_time=600,
    cost=140000,
    runningcost=0,
    fixed_cost=117,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/bulk-rch-12t.blend',
    upstream_dat='trains/wagon-bulk-rch-12t.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
