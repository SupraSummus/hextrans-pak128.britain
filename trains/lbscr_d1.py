"""lbscr-d1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-D1',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1873,
    intro_month=11,
    retire_year=1892,
    retire_month=7,
    speed=105,
    length=5,
    weight=43,
    axle_load=16,
    power=181,
    tractive_effort=60,
    payload=0,
    cost=6630000,
    runningcost=214,
    fixed_cost=29525,
    increase_maintenance_after_years=40,
    years_before_maintenance_max_reached=35,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-d1-malachite.blend',
    upstream_dat='trains/lbscr-d1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
