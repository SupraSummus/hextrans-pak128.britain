"""gnr-q."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gnr-q',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1886,
    intro_month=12,
    retire_year=1897,
    retire_month=2,
    speed=140,
    length=4,
    weight=40,
    axle_load=17,
    power=208,
    tractive_effort=53,
    payload=0,
    cost=14750000,
    runningcost=141,
    fixed_cost=36292,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['GNR-Stirling8Foot-Tender'],
    blend='trains/Locomotives/gnr-q.blend',
    upstream_dat='trains/gnr-q.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
