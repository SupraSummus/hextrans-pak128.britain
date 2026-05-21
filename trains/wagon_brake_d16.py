"""wagon-brake-d16."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.lnwrs.org.uk/Wagons/brakes/Diag016.php
SPEC = Vehicle(
    name='BrakeD16',
    waytype='track',
    copyright='James',
    freight='Bucher',
    intro_year=1880,
    intro_month=2,
    retire_year=1903,
    retire_month=4,
    speed=80,
    length=3,
    weight=10.0,
    brake_force=3,
    rolling_resistance=19,
    payload=0,
    cost=120000,
    runningcost=0,
    fixed_cost=4850,
    bidirectional=1,
    blend='trains/Wagons/brake-d16.blend',
    upstream_dat='trains/wagon-brake-d16.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
