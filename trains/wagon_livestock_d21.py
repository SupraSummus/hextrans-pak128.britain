"""wagon-livestock-d21."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.lnwrs.org.uk/Wagons/cattle/Diag021.php
SPEC = Vehicle(
    name='LivestockD21',
    waytype='track',
    copyright='James',
    freight='livestock',
    intro_year=1855,
    intro_month=5,
    retire_year=1903,
    retire_month=7,
    speed=56,
    length=3,
    weight=6.8,
    axle_load=8,
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
    blend='trains/Wagons/livestock-d21.blend',
    upstream_dat='trains/wagon-livestock-d21.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
