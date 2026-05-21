"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LivestockEarly3',
    waytype='track',
    copyright='JamesPetts',
    freight='livestock',
    intro_year=1828,
    intro_month=12,
    retire_year=1855,
    retire_month=5,
    speed=40,
    length=2,
    weight=2,
    axle_load=1,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=3250,
    payload=5,
    min_loading_time=300,
    max_loading_time=900,
    cost=77000,
    runningcost=0,
    fixed_cost=128,
    bidirectional=1,
    blend='trains/Wagons/livestock-early3.blend',
    upstream_dat='trains/wagon-livestock-early3.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
