"""lbscr-e5."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-E5',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1902,
    intro_month=11,
    retire_year=1919,
    retire_month=7,
    speed=100,
    length=6,
    weight=60,
    axle_load=17,
    power=257,
    tractive_effort=77,
    payload=0,
    cost=4023300,
    runningcost=105,
    fixed_cost=27353,
    years_before_maintenance_max_reached=27,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-E5-malachite.blend',
    upstream_dat='trains/lbscr-e5.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
