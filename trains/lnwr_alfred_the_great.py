"""lnwr-alfred-the-great."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# These were also called the "Benbow class" afer a modification.
SPEC = Vehicle(
    name='LNWR-Alfred-the-Great',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1901,
    intro_month=3,
    retire_year=1904,
    retire_month=3,
    speed=142,
    length=6,
    weight=55,
    axle_load=16,
    power=259,
    tractive_effort=136,
    way_wear_factor=68750,
    payload=0,
    cost=8600000,
    runningcost=112,
    fixed_cost=31167,
    increase_maintenance_after_years=17,
    years_before_maintenance_max_reached=21,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-PrinceOfWales-Tender'],
    liverytype=['LNWR-Black', 'LMS-Standard'],
    upgrade=['LNWR-Renown'],
    blend='trains/Locomotives/lnwr-alfred-the-great-lms.blend',
    upstream_dat='trains/lnwr-alfred-the-great.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
