"""lnwr-45ft-full-brake."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-45ft-cor-full-brake',
    waytype='track',
    copyright='Kieron/jamespetts',
    freight='Post',
    intro_year=1895,
    intro_month=1,
    retire_year=1907,
    retire_month=4,
    speed=160,
    length=8,
    weight=23,
    axles=4,
    payload=270,
    min_loading_time=35,
    max_loading_time=90,
    cost=520000,
    runningcost=0,
    fixed_cost=619,
    bidirectional=1,
    can_lead_from_rear=0,
    liverytype=['LNWR-Black', 'LMS-Standard'],
    blend='trains/Carriages/lnwr-45ft-cor-full-brake-lms.blend',
    upstream_dat='trains/lnwr-45ft-full-brake.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
