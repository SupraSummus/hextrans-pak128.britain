"""wagon-tea."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='Bogie Tanker(TEA)',
    waytype='track',
    copyright='Kieron',
    freight='Oel',
    intro_year=1970,
    intro_month=2,
    speed=96,
    length=10,
    weight=24,
    axle_load=22,
    way_wear_factor=127500,
    payload=78,
    min_loading_time=480,
    max_loading_time=600,
    cost=340000,
    runningcost=0,
    fixed_cost=142,
    bidirectional=1,
    can_lead_from_rear=0,
    blend='trains/Wagons/tea.blend',
    upstream_dat='trains/wagon-tea.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
