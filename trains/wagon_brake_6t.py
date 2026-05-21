"""wagon-brake-6t."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://myweb.tiscali.co.uk/gansg/4-rstock/04arstock1.htm
SPEC = Vehicle(
    name='brake-6t',
    waytype='track',
    copyright='James/JamesPetts',
    freight='Bucher',
    intro_year=1841,
    intro_month=4,
    retire_year=1863,
    retire_month=1,
    speed=56,
    length=3,
    weight=6,
    brake_force=1,
    rolling_resistance=19,
    payload=0,
    cost=110000,
    runningcost=0,
    fixed_cost=4892,
    bidirectional=1,
    blend='trains/Wagons/brake-6t.blend',
    upstream_dat='trains/wagon-brake-6t.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
