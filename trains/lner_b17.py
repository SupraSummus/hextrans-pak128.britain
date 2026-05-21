"""lner-b17."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-B17',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1928,
    intro_month=11,
    retire_year=1937,
    retire_month=6,
    speed=150,
    length=7,
    weight=77,
    axle_load=18,
    power=492,
    tractive_effort=100,
    way_wear_factor=105875,
    payload=0,
    cost=8467200,
    runningcost=245,
    fixed_cost=31056,
    increase_maintenance_after_years=18,
    years_before_maintenance_max_reached=14,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['LNER-B17-Tender'],
    liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lner-b17-5-wartime.blend',
    upstream_dat='trains/lner-b17.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
