"""milk-van."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Passenger rated milk/food van
SPEC = Vehicle(
    name='milk-van',
    waytype='track',
    copyright='James',
    freight='meat',
    intro_year=1865,
    intro_month=3,
    retire_year=1885,
    retire_month=2,
    speed=80,
    length=4,
    weight=5,
    axle_load=5,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=11375,
    payload=10,
    min_loading_time=300,
    max_loading_time=900,
    cost=90000,
    runningcost=0,
    fixed_cost=38,
    upgrade_price=12250,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Carriages/lbscr-6wheel-fruit-and-milk-van-olive.blend',
    upstream_dat='trains/milk-van.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
