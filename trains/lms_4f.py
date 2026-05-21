"""lms-4f."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-4F',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1911,
    intro_month=6,
    retire_year=1941,
    retire_month=4,
    speed=95,
    length=6,
    weight=50,
    axles=3,
    power=307,
    tractive_effort=109,
    payload=0,
    cost=3696000,
    runningcost=125,
    fixed_cost=27080,
    increase_maintenance_after_years=17,
    years_before_maintenance_max_reached=14,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LMS-4F-Tender'],
    liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lms-4f-tender.blend',
    upstream_dat='trains/lms-4f.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
