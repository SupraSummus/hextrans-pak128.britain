"""brake-6w-15t."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Based on the Highland Railway "type B" brake van:
# see Tatlow pp. 179-180
SPEC = Vehicle(
    name='brake-6w-15t',
    waytype='track',
    copyright='James',
    freight='Bucher',
    intro_year=1883,
    intro_month=5,
    retire_year=1915,
    retire_month=7,
    speed=80,
    length=5,
    weight=15.0,
    axles=3,
    brake_force=5,
    rolling_resistance=20,
    payload=0,
    cost=150000,
    runningcost=0,
    fixed_cost=4850,
    bidirectional=1,
    blend='trains/Wagons/brake-6w-15t.blend',
    upstream_dat='trains/brake-6w-15t.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
