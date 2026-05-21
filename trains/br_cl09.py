"""br-cl09."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class09',
    waytype='track',
    copyright='Junna/Cake',
    freight='None',
    engine_type='diesel',
    intro_year=1959,
    intro_month=9,
    retire_year=1962,
    retire_month=10,
    speed=44,
    length=6,
    weight=49,
    axles=3,
    power=298,
    gear=50,
    tractive_effort=111,
    rolling_resistance=10,
    payload=0,
    cost=445000,
    runningcost=298,
    fixed_cost=10464,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='spompeytransportvideo-class-08.wav',
    constraint_prev=['none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/br-cl09-green.blend',
    upstream_dat='trains/br-cl09.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
