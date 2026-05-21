"""lbscr-e1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-E1',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1874,
    intro_month=11,
    retire_year=1891,
    retire_month=12,
    speed=85,
    length=6,
    weight=45,
    axles=3,
    power=186,
    tractive_effort=78,
    way_wear_factor=70875,
    payload=0,
    cost=4400000,
    runningcost=194,
    fixed_cost=27667,
    increase_maintenance_after_years=40,
    years_before_maintenance_max_reached=35,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-e1-goods-green.blend',
    upstream_dat='trains/lbscr-e1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
