"""wagon-piece-d88."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# These are based on the LNWR D88 introduced in 1908:
# http://www.lnwrs.org.uk/Wagons/vans/Diag088.php
# However, functionally similar vans to diagram 87
# were introduced in 1903, and it does not make sense
# to represent both: http://www.lnwrs.org.uk/Wagons/vans/Diag087.php
SPEC = Vehicle(
    name='PieceD88',
    waytype='track',
    copyright='James',
    freight='Bucher',
    intro_year=1903,
    intro_month=6,
    retire_year=1931,
    retire_month=6,
    speed=56,
    length=3,
    weight=7,
    axle_load=7,
    brake_force=0,
    rolling_resistance=18,
    way_wear_factor=21350,
    payload=12,
    min_loading_time=300,
    max_loading_time=900,
    cost=120000,
    runningcost=0,
    fixed_cost=50,
    bidirectional=1,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/piece-d88.blend',
    upstream_dat='trains/wagon-piece-d88.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
