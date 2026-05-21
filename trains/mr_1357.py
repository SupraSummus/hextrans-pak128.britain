"""mr-1357."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-1357',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1878,
    intro_month=2,
    retire_year=1891,
    retire_month=6,
    speed=87,
    length=5,
    weight=38,
    axles=3,
    power=209,
    tractive_effort=65,
    way_wear_factor=58950,
    payload=0,
    cost=3808000,
    runningcost=209,
    fixed_cost=27173,
    increase_maintenance_after_years=40,
    years_before_maintenance_max_reached=40,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-Kirtley156Tender'],
    liverytype=['MR-Early', 'MR-Standard'],
    blend='trains/Locomotives/mr-1357-class-green-too-small.blend',
    upstream_dat='trains/mr-1357.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
