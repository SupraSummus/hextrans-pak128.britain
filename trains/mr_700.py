"""mr-700."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-700',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1869,
    intro_month=4,
    retire_year=1878,
    retire_month=2,
    speed=86,
    length=5,
    weight=36,
    axles=3,
    power=190,
    tractive_effort=53,
    brake_force=0,
    way_wear_factor=56700,
    payload=0,
    cost=7015000,
    runningcost=229,
    fixed_cost=29846,
    increase_maintenance_after_years=40,
    years_before_maintenance_max_reached=40,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-Kirtley156Tender'],
    liverytype=['MR-Early', 'MR-Standard'],
    blend='trains/Locomotives/mr-700-class-green.blend',
    upstream_dat='trains/mr-700.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
