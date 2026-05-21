"""lbscr-c2x."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-C2x',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1908,
    intro_month=9,
    retire_year=1940,
    retire_month=1,
    speed=100,
    length=4,
    weight=45.7,
    axles=3,
    power=267,
    tractive_effort=85,
    payload=0,
    cost=3020000,
    runningcost=106,
    fixed_cost=26517,
    upgrade_price=1300000,
    bidirectional=0,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LBSCR-C2-tender'],
    liverytype=['LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-c2x-austerity.blend',
    upstream_dat='trains/lbscr-c2x.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
