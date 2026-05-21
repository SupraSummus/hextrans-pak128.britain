"""wagon-tanker-rch."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='RCH-Tanker',
    waytype='track',
    copyright='Kieron',
    freight='Oel',
    intro_year=1909,
    intro_month=12,
    retire_year=1964,
    retire_month=10,
    speed=56,
    length=3,
    weight=11,
    axle_load=17,
    brake_force=0,
    rolling_resistance=18,
    way_wear_factor=41500,
    payload=26,
    min_loading_time=480,
    max_loading_time=600,
    cost=165000,
    runningcost=0,
    fixed_cost=138,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    blend='trains/Wagons/tanker-rch.blend',
    upstream_dat='trains/wagon-tanker-rch.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
