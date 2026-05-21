"""lbscr-e4."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-E4',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1897,
    intro_month=5,
    retire_year=1903,
    retire_month=9,
    speed=97,
    length=6,
    weight=57,
    axle_load=16,
    power=225,
    tractive_effort=85,
    payload=0,
    cost=3661203,
    runningcost=141,
    fixed_cost=27051,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-E4-br.blend',
    upstream_dat='trains/lbscr-e4.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
