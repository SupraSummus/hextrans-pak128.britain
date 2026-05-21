"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Wagon3CarBogie',
    waytype='track',
    copyright='James',
    freight='Autos',
    intro_year=1950,
    intro_month=4,
    retire_year=1973,
    retire_month=7,
    speed=80,
    length=7,
    weight=12,
    axle_load=4,
    way_wear_factor=21750,
    payload=3,
    min_loading_time=240,
    max_loading_time=480,
    cost=500000,
    runningcost=0,
    fixed_cost=208,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/3-car-bogie.blend',
    upstream_dat='trains/wagon-3-car-bogie.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
