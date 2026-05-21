"""wagon-brake-d93."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.lnwrs.org.uk/Wagons/brakes/Diag018.php
SPEC = Vehicle(
    name='BrakeD93',
    waytype='track',
    copyright='James',
    freight='Bucher',
    intro_year=1903,
    intro_month=1,
    retire_year=1926,
    retire_month=8,
    speed=80,
    length=4,
    weight=20.0,
    brake_force=7,
    rolling_resistance=19,
    payload=0,
    cost=140000,
    runningcost=0,
    fixed_cost=4850,
    bidirectional=1,
    blend='trains/Wagons/brake-d93.blend',
    upstream_dat='trains/wagon-brake-d93.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
