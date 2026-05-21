"""lbscr-e3."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-E3',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1891,
    intro_month=1,
    retire_year=1902,
    retire_month=5,
    speed=85,
    length=6,
    weight=57.7,
    axle_load=16,
    power=220,
    tractive_effort=89,
    payload=0,
    cost=3651000,
    runningcost=141,
    fixed_cost=27043,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-E3-malachite.blend',
    upstream_dat='trains/lbscr-e3.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
