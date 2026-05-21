"""lms-patriot."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-Patriot',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1930,
    intro_month=11,
    retire_year=1935,
    retire_month=7,
    speed=150,
    length=7,
    weight=81,
    axle_load=20,
    power=431,
    tractive_effort=118,
    way_wear_factor=111375,
    payload=0,
    cost=6624000,
    runningcost=258,
    fixed_cost=45520,
    increase_maintenance_after_years=24,
    years_before_maintenance_max_reached=11,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['LMS-Patriot-Tender'],
    liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lms-patriot-tender-wartime.blend',
    upstream_dat='trains/lms-patriot.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
