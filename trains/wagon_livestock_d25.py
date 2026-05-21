"""wagon-livestock-d25."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.lnwrs.org.uk/Wagons/cattle/Diag025.php
# Strictly, these were prize cattle vans; it is hard
# to find information about late 19th century general
# cattle vans.
SPEC = Vehicle(
    name='LivestockD25',
    waytype='track',
    copyright='James',
    freight='livestock',
    intro_year=1899,
    intro_month=9,
    retire_year=1931,
    retire_month=2,
    speed=56,
    length=3,
    weight=7.5,
    axle_load=4,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=10550,
    payload=12,
    min_loading_time=300,
    max_loading_time=900,
    cost=120000,
    runningcost=0,
    fixed_cost=50,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/livestock-d25.blend',
    upstream_dat='trains/wagon-livestock-d25.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
