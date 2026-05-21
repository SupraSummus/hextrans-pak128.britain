"""lmr-planet."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.steamlocomotive.com/locobase.php?country=Great_Britain&wheel=2-2-0&railroad=lm
SPEC = Vehicle(
    name='LMR-Planet',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1830,
    intro_month=6,
    retire_year=1839,
    retire_month=9,
    speed=59,
    length=3,
    weight=8.1,
    axle_load=5,
    power=18,
    tractive_effort=4,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=14600,
    payload=0,
    cost=4752000,
    runningcost=61,
    fixed_cost=22600,
    increase_maintenance_after_years=25,
    years_before_maintenance_max_reached=70,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LMR-Planet-Tender'],
    blend='trains/Locomotives/planet.blend',
    upstream_dat='trains/lmr-planet.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
