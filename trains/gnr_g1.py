"""gnr-g1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gnr-g1',
    waytype='track',
    copyright='=Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1884,
    intro_month=6,
    retire_year=1894,
    retire_month=1,
    speed=135,
    length=5,
    weight=40,
    axle_load=15,
    power=209,
    tractive_effort=54,
    payload=0,
    cost=13150000,
    runningcost=141,
    fixed_cost=34958,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['GNR-Stirling8Foot-Tender'],
    upgrade=['gnr-g2', 'gnr-g3'],
    blend='trains/Locomotives/gnr-g1-lner.blend',
    upstream_dat='trains/gnr-g1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
