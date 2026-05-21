"""lnwr-george-V."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-George-V',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1910,
    intro_month=5,
    retire_year=1915,
    retire_month=12,
    speed=147,
    length=6,
    weight=61,
    axle_load=19,
    power=324,
    tractive_effort=92,
    payload=0,
    cost=10200000,
    runningcost=140,
    fixed_cost=48500,
    increase_maintenance_after_years=28,
    years_before_maintenance_max_reached=18,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-PrinceOfWales-Tender'],
    liverytype=['LNWR-Black', 'LMS-Standard'],
    blend='trains/Locomotives/lnwr-george-V-lms.blend',
    upstream_dat='trains/lnwr-george-V.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
