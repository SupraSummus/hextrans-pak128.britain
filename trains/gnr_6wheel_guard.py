"""gnr-6wheel-guard."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GNR-6Wheel-Guard',
    waytype='track',
    copyright='Kieron',
    freight='Post',
    intro_year=1876,
    intro_month=8,
    retire_year=1909,
    retire_month=11,
    speed=150,
    length=6,
    weight=14,
    axles=3,
    payload=320,
    min_loading_time=35,
    max_loading_time=90,
    cost=314000,
    runningcost=0,
    fixed_cost=374,
    bidirectional=1,
    can_lead_from_rear=0,
    liverytype=['GNR-Standard', 'LNER-Standard'],
    blend='trains/Carriages/gnr-6wheel-guard.blend',
    upstream_dat='trains/gnr-6wheel-guard.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
