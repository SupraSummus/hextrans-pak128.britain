"""lmr-planet-goods."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMR-Planet-Goods',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1830,
    intro_month=6,
    retire_year=1839,
    retire_month=9,
    speed=42,
    length=3,
    weight=10.1,
    power=10,
    tractive_effort=7,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=20958,
    payload=0,
    cost=4752000,
    runningcost=35,
    fixed_cost=22600,
    increase_maintenance_after_years=25,
    years_before_maintenance_max_reached=70,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LMR-Planet-Tender'],
    blend='trains/Locomotives/planet.blend',
    upstream_dat='trains/lmr-planet-goods.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
