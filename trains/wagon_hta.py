"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Bulk Hopper(HTA)',
    waytype='track',
    copyright='Kieron',
    freight='Kohle',
    intro_year=2001,
    intro_month=3,
    speed=120,
    length=10,
    weight=27,
    axle_load=26,
    brake_force=20,
    way_wear_factor=127500,
    payload=75,
    min_loading_time=120,
    max_loading_time=120,
    cost=690000,
    runningcost=0,
    fixed_cost=288,
    bidirectional=1,
    blend='trains/Wagons/hta.blend',
    upstream_dat='trains/wagon-hta.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
