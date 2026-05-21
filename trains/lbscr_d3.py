"""lbscr-d3."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-D3',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1892,
    intro_month=5,
    retire_year=1897,
    retire_month=11,
    speed=95,
    length=6,
    weight=52.8,
    axle_load=15,
    power=213,
    tractive_effort=78,
    payload=0,
    cost=3790000,
    runningcost=139,
    fixed_cost=27158,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-d3-austerity.blend',
    upstream_dat='trains/lbscr-d3.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
