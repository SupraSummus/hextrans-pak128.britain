"""mr-1377."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.steamlocomotive.com/locobase.php?country=Great_Britain&wheel=0-6-0&railroad=midland
SPEC = Vehicle(
    name='MR-1377',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1878,
    intro_month=1,
    retire_year=1899,
    retire_month=2,
    speed=85,
    length=5,
    weight=40,
    axles=3,
    power=209,
    tractive_effort=67,
    way_wear_factor=63000,
    payload=0,
    cost=3408000,
    runningcost=209,
    fixed_cost=26840,
    increase_maintenance_after_years=30,
    years_before_maintenance_max_reached=20,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['MR-Early', 'MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/mr-1377-class-green.blend',
    upstream_dat='trains/mr-1377.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
