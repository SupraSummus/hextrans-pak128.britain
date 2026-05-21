"""4wheel-1850s-brake."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='4-wheel-1850s-brake',
    waytype='track',
    copyright='James/jamespetts',
    freight='Post',
    intro_year=1850,
    intro_month=9,
    retire_year=1859,
    retire_month=10,
    speed=135,
    length=3,
    weight=8.0,
    axles=2,
    brake_force=2,
    rolling_resistance=19,
    payload=50,
    min_loading_time=35,
    max_loading_time=55,
    cost=144000,
    runningcost=0,
    fixed_cost=4920,
    bidirectional=1,
    can_lead_from_rear=0,
    liverytype=['LNWR-Early', 'MR-Early', 'MR-Standard', 'GNR-early', 'LSWR-Indian-red', 'GWR-early', 'GWR-two-tone'],
    blend='trains/Carriages/4wheel-1850.blend',
    upstream_dat='trains/4wheel-1850s-brake.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
