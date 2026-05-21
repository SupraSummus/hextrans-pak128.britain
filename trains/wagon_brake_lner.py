"""wagon-brake-lner."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BrakeLNER',
    waytype='track',
    copyright='James/JamesPetts',
    freight='Bucher',
    intro_year=1926,
    intro_month=2,
    retire_year=1950,
    retire_month=6,
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
    blend='trains/Wagons/brake-lner.blend',
    upstream_dat='trains/wagon-brake-lner.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
