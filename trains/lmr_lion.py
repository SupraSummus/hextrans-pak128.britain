"""lmr-lion."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMR-Lion',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1837,
    intro_month=10,
    retire_year=1845,
    retire_month=8,
    speed=45,
    length=3,
    weight=16.5,
    axle_load=6,
    power=40,
    tractive_effort=9,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=31988,
    payload=0,
    cost=4640000,
    runningcost=101,
    fixed_cost=22444,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LMR-Planet-Tender'],
    blend='trains/Locomotives/lion.blend',
    upstream_dat='trains/lmr-lion.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
