"""lmr-rocket."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.steamlocomotive.com/locobase.php?country=Great_Britain&wheel=2-2-0&railroad=lm
SPEC = Vehicle(
    name='LMR-Rocket',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1829,
    intro_month=8,
    retire_year=1835,
    retire_month=10,
    speed=48,
    length=2,
    weight=5,
    axle_load=3,
    power=12,
    tractive_effort=4,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=9375,
    payload=0,
    cost=5544000,
    runningcost=42,
    fixed_cost=23700,
    increase_maintenance_after_years=25,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LMR-Rocket-Tender'],
    blend='trains/Locomotives/rocket.blend',
    upstream_dat='trains/lmr-rocket.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
