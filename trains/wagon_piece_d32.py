"""wagon-piece-d32."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.lnwrs.org.uk/Wagons/vans/Diag032.php
SPEC = Vehicle(
    name='PieceD32',
    waytype='track',
    copyright='James',
    freight='Bucher',
    intro_year=1855,
    intro_month=6,
    retire_year=1908,
    retire_month=12,
    speed=56,
    length=3,
    weight=5.5,
    axle_load=5,
    brake_force=0,
    rolling_resistance=19,
    payload=8,
    min_loading_time=300,
    max_loading_time=900,
    cost=100000,
    runningcost=0,
    fixed_cost=42,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/piece-d32.blend',
    upstream_dat='trains/wagon-piece-d32.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
