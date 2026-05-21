"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LivestockEarly1',
    waytype='track',
    copyright='James',
    freight='livestock',
    intro_year=1763,
    intro_month=1,
    retire_year=1918,
    retire_month=11,
    speed=25,
    length=2,
    weight=1,
    axle_load=1,
    brake_force=0,
    rolling_resistance=20,
    way_wear_factor=1550,
    payload=2,
    min_loading_time=300,
    max_loading_time=900,
    cost=46000,
    runningcost=0,
    fixed_cost=19,
    bidirectional=1,
    blend='trains/Wagons/livestock-early1.blend',
    upstream_dat='trains/wagon-livestock-early1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
