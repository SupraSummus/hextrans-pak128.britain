"""wagon-passenger."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='passenger-wagon',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='Passagiere',
    intro_year=1807,
    intro_month=3,
    retire_year=1833,
    retire_month=1,
    speed=20,
    length=2,
    weight=1,
    axle_load=1,
    brake_force=0,
    rolling_resistance=19,
    payload=8,
    min_loading_time=20,
    max_loading_time=60,
    cost=46000,
    runningcost=0,
    fixed_cost=19,
    bidirectional=1,
    payload_by_class=[0, 0, 8],
    comfort_by_class=[0, 0, 11],
    blend='trains/Carriages/wagon-passenger.blend',
    upstream_dat='trains/wagon-passenger.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
