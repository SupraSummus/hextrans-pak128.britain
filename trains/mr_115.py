"""mr-115."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-Spinner',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1896,
    intro_month=2,
    retire_year=1900,
    retire_month=1,
    speed=145,
    length=4,
    weight=47,
    axle_load=19,
    power=268,
    tractive_effort=68,
    payload=0,
    cost=5404500,
    runningcost=182,
    fixed_cost=28504,
    increase_maintenance_after_years=34,
    years_before_maintenance_max_reached=20,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['MR-Spinner-Tender'],
    blend='trains/Locomotives/mr-115-class.blend',
    upstream_dat='trains/mr-115.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
