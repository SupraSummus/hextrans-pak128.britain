"""lner-b17-5."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-B17-5',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1937,
    intro_month=6,
    retire_year=1948,
    retire_month=1,
    speed=150,
    length=7,
    weight=81,
    axle_load=18,
    power=416,
    tractive_effort=100,
    way_wear_factor=111375,
    payload=0,
    cost=8467200,
    runningcost=240,
    fixed_cost=31056,
    increase_maintenance_after_years=14,
    years_before_maintenance_max_reached=11,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['LNER-B17-5-Tender'],
    liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lner-b17-5.blend',
    upstream_dat='trains/lner-b17-5.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
