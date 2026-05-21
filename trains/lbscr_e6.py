"""lbscr-e6."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-E6',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1904,
    intro_month=12,
    retire_year=1921,
    retire_month=9,
    speed=88,
    length=6,
    weight=62,
    axle_load=16,
    power=257,
    tractive_effort=94,
    payload=0,
    cost=4500000,
    runningcost=106,
    fixed_cost=27750,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-e6-goods-green.blend',
    upstream_dat='trains/lbscr-e6.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
