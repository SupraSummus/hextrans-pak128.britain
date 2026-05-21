"""mr-480."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-480',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1863,
    intro_month=12,
    retire_year=1869,
    retire_month=4,
    speed=85,
    length=4,
    weight=32,
    axles=3,
    power=273,
    tractive_effort=50,
    brake_force=0,
    rolling_resistance=17,
    way_wear_factor=66400,
    payload=0,
    cost=13302000,
    runningcost=275,
    fixed_cost=35085,
    increase_maintenance_after_years=40,
    years_before_maintenance_max_reached=40,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-Kirtley156Tender'],
    liverytype=['MR-Early', 'MR-Standard'],
    blend='trains/Locomotives/mr-480-green.blend',
    upstream_dat='trains/mr-480.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
