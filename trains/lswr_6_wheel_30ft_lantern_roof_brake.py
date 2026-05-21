"""lswr-6-wheel-30ft-lantern-roof-brake."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.ragstonemodels.co.uk/london--south-western-railway.html
SPEC = Vehicle(
    name='lswr-6-wheel-30ft-lantern-roof-brake',
    waytype='track',
    copyright='JamesPetts',
    freight='Post',
    intro_year=1882,
    intro_month=5,
    retire_year=1887,
    retire_month=8,
    speed=150,
    length=5,
    weight=13.1,
    axles=3,
    payload=240,
    min_loading_time=35,
    max_loading_time=85,
    cost=335500,
    runningcost=0,
    fixed_cost=5199,
    bidirectional=1,
    can_lead_from_rear=0,
    liverytype=['LSWR-pea-green', 'LSWR-sage', 'SR-Olive-Green'],
    blend='trains/Carriages/lswr-6-wheel-30ft.blend',
    upstream_dat='trains/lswr-6-wheel-30ft-lantern-roof-brake.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
