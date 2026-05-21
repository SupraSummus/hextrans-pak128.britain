"""lbscr-0-4-2t."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-0-4-2T',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1855,
    intro_month=8,
    retire_year=1866,
    retire_month=3,
    speed=78,
    length=4,
    weight=20,
    axles=3,
    power=95,
    tractive_effort=26,
    brake_force=7,
    rolling_resistance=19,
    way_wear_factor=41500,
    payload=0,
    cost=7010000,
    runningcost=128,
    fixed_cost=29842,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Craven', 'LBSCR-Stroudley'],
    blend='trains/Locomotives/lbscr-0-4-2swt-craven.blend',
    upstream_dat='trains/lbscr-0-4-2t.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
