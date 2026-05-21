"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Wagon2CarFlat',
    waytype='track',
    copyright='James',
    freight='Autos',
    intro_year=1910,
    intro_month=3,
    retire_year=1960,
    retire_month=2,
    speed=56,
    length=4,
    weight=7,
    axle_load=5,
    brake_force=0,
    way_wear_factor=13250,
    payload=2,
    min_loading_time=240,
    max_loading_time=480,
    cost=140000,
    runningcost=0,
    fixed_cost=117,
    bidirectional=10,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/2-car-flat.blend',
    upstream_dat='trains/wagon-2-car-flat.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
