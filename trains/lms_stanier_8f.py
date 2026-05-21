"""lms-stanier-8f."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-Stanier-8F',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1935,
    intro_month=3,
    retire_year=1946,
    retire_month=1,
    speed=90,
    length=7,
    weight=72,
    axle_load=17,
    power=437,
    tractive_effort=144,
    payload=0,
    cost=5940000,
    runningcost=241,
    fixed_cost=28950,
    increase_maintenance_after_years=16,
    years_before_maintenance_max_reached=9,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['LMS-Stanier-8F-Tender'],
    liverytype=['LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lms-stanier-0-4-4T-br.blend',
    upstream_dat='trains/lms-stanier-8f.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
