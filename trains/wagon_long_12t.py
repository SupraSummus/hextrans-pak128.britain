"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Long12T',
    waytype='track',
    copyright='James',
    freight='Bretter',
    intro_year=1902,
    intro_month=2,
    retire_year=1948,
    retire_month=5,
    speed=56,
    length=3,
    weight=7,
    axle_load=9,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=23750,
    payload=12,
    min_loading_time=360,
    max_loading_time=975,
    cost=140000,
    runningcost=0,
    fixed_cost=167,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/long-12t.blend',
    upstream_dat='trains/wagon-long-12t.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
