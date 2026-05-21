"""lswr-700-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-700-class-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1919,
    intro_month=6,
    retire_year=1927,
    retire_month=12,
    speed=85,
    length=5,
    weight=47.5,
    axles=3,
    power=257,
    tractive_effort=105,
    payload=0,
    cost=4650000,
    runningcost=147,
    fixed_cost=27875,
    upgrade_price=930000,
    bidirectional=0,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LSWR-700-class-tender'],
    liverytype=['LSWR-royal-green', 'SR-Olive-Green', 'BR-Early'],
    blend='trains/Locomotives/lswr-700-class-br.blend',
    upstream_dat='trains/lswr-700-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
