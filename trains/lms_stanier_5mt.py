"""lms-stanier-5mt."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-Stanier-5MT',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1934,
    intro_month=5,
    retire_year=1951,
    retire_month=4,
    speed=135,
    length=7,
    weight=72,
    axle_load=19,
    power=451,
    tractive_effort=113,
    payload=0,
    cost=4598000,
    runningcost=252,
    fixed_cost=27832,
    increase_maintenance_after_years=10,
    years_before_maintenance_max_reached=13,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['LMS-Stanier-5MT-Tender'],
    liverytype=['LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lms-stanier-0-4-4T-br.blend',
    upstream_dat='trains/lms-stanier-5mt.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
