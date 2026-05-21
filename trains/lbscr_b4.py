"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lbscr-b4.blend'
_UPSTREAM_DAT = 'trains/lbscr-b4.dat'

SPECS = [
Vehicle(
    name='LBSCR-B4',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1899,
    intro_month=12,
    retire_year=1905,
    retire_month=11,
    speed=145,
    length=4,
    weight=49,
    axle_load=17,
    power=352,
    tractive_effort=79,
    payload=0,
    cost=7000000,
    runningcost=198,
    fixed_cost=45833,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LBSCR-B4-tender'],
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    upgrade=['LBSCR-B4x'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='LBSCR-B4-tender',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1899,
    intro_month=12,
    retire_year=1905,
    retire_month=11,
    speed=150,
    length=4,
    weight=32,
    axles=3,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    constraint_prev=['LBSCR-B4', 'LBSCR-B4x'],
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
