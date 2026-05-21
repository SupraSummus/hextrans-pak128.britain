"""gnr-g3."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gnr-g3',
    waytype='track',
    copyright='=Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1900,
    intro_month=11,
    retire_year=1908,
    retire_month=9,
    speed=140,
    length=5,
    weight=50.3,
    axle_load=20,
    power=250,
    tractive_effort=68,
    payload=0,
    cost=13560000,
    runningcost=109,
    fixed_cost=35300,
    upgrade_price=2750000,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['GNR-Stirling8Foot-Tender'],
    blend='trains/Locomotives/gnr-g3.blend',
    upstream_dat='trains/gnr-g3.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
