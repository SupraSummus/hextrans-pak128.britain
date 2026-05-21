"""wagon-piece-zsx."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='PieceZSX',
    waytype='track',
    copyright='James',
    freight='Bucher',
    intro_year=1963,
    intro_month=2,
    retire_year=1993,
    retire_month=7,
    speed=120,
    length=6,
    weight=12,
    axle_load=12,
    way_wear_factor=40200,
    payload=24,
    min_loading_time=300,
    max_loading_time=900,
    cost=600000,
    runningcost=0,
    fixed_cost=333,
    bidirectional=1,
    blend='trains/Wagons/piece-zsx.blend',
    upstream_dat='trains/wagon-piece-zsx.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
