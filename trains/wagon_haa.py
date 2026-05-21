"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Bulk Hopper(HAA)',
    waytype='track',
    copyright='Kieron',
    freight='Kohle',
    intro_year=1965,
    intro_month=3,
    retire_year=2005,
    retire_month=5,
    speed=95,
    length=5,
    weight=13,
    axle_load=22,
    way_wear_factor=56250,
    payload=32,
    min_loading_time=120,
    max_loading_time=120,
    cost=400000,
    runningcost=0,
    fixed_cost=333,
    bidirectional=1,
    blend='trains/Wagons/haa.blend',
    upstream_dat='trains/wagon-haa.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
