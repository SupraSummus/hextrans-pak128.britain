"""ger-claud."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GER-Claud-Hamilton',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1900,
    intro_month=2,
    retire_year=1903,
    retire_month=9,
    speed=145,
    length=6,
    weight=51.1,
    axle_load=17,
    power=299,
    tractive_effort=76,
    payload=0,
    cost=6462800,
    runningcost=129,
    fixed_cost=45386,
    increase_maintenance_after_years=27,
    years_before_maintenance_max_reached=25,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['GER-Claud-Hamilton-Tender'],
    liverytype=['GER-Ultramarine', 'WW1-Austerity', 'LNER-Standard', 'WW2-Austerity', 'BR-Early'],
    upgrade=['ger-super-claud'],
    blend='trains/Locomotives/ger-claud-wartime.blend',
    upstream_dat='trains/ger-claud.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
