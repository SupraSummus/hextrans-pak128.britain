"""wagon-brake-sr."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# TODO: This may be set up as the bogie brake van,
# but the graphics are for the rigid version.
# Consider adding a bogie version, too.
SPEC = Vehicle(
    name='BrakeSR',
    waytype='track',
    copyright='James/JamesPetts',
    freight='Post',
    intro_year=1923,
    intro_month=10,
    retire_year=1950,
    retire_month=12,
    speed=100,
    length=3,
    weight=25,
    brake_force=8,
    rolling_resistance=19,
    payload=50,
    min_loading_time=15,
    max_loading_time=30,
    cost=200000,
    runningcost=0,
    fixed_cost=4802,
    bidirectional=1,
    can_lead_from_rear=0,
    blend='trains/Wagons/brake-SR.blend',
    upstream_dat='trains/wagon-brake-sr.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
