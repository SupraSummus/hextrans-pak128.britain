"""lms-princess-royal."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-Princess-Royal',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1933,
    intro_month=6,
    retire_year=1951,
    retire_month=4,
    speed=155,
    length=8,
    weight=106.2,
    axle_load=21,
    power=606,
    tractive_effort=179,
    way_wear_factor=139388,
    payload=0,
    cost=9849600,
    runningcost=389,
    fixed_cost=60520,
    increase_maintenance_after_years=6,
    years_before_maintenance_max_reached=10,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['LMS-Princess-Royal-Tender'],
    liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lms-princess-coronation-non-streamlined-br.blend',
    upstream_dat='trains/lms-princess-royal.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
