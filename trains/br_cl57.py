"""br-cl57."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class57',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='diesel',
    intro_year=1997,
    intro_month=2,
    retire_year=2007,
    retire_month=6,
    speed=153,
    length=11,
    weight=121,
    axles=6,
    power=2050,
    gear=50,
    tractive_effort=245,
    rolling_resistance=13,
    payload=0,
    cost=6912000,
    runningcost=615,
    fixed_cost=13600,
    upgrade_price=1974857,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='video47-class-57.wav',
    constraint_prev=['BR-Class57', 'none'],
    blend='trains/Locomotives/br-cl57-fgw.blend',
    upstream_dat='trains/br-cl57.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
