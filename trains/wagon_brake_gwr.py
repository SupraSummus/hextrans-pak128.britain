"""wagon-brake-gwr."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.gwr.org.uk/nobrakes.html
# Scaled as a 18ft 4 wheeled brake van
SPEC = Vehicle(
    name='BrakeGWR',
    waytype='track',
    copyright='James',
    freight='Bucher',
    intro_year=1920,
    intro_month=8,
    retire_year=1950,
    retire_month=9,
    speed=100,
    length=3,
    weight=20,
    brake_force=7,
    rolling_resistance=19,
    payload=0,
    cost=180000,
    runningcost=0,
    fixed_cost=4850,
    bidirectional=1,
    blend='trains/Wagons/brake-GWR.blend',
    upstream_dat='trains/wagon-brake-gwr.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
