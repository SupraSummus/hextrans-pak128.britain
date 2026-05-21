"""lner-a4."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-A4',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1935,
    intro_month=4,
    retire_year=1948,
    retire_month=1,
    speed=160,
    length=8,
    weight=104.6,
    axle_load=22,
    power=687,
    tractive_effort=158,
    way_wear_factor=143825,
    payload=0,
    cost=11088000,
    runningcost=395,
    fixed_cost=63100,
    increase_maintenance_after_years=12,
    years_before_maintenance_max_reached=12,
    smoke='Steam',
    sound='the-mart-ban-lner-a4.wav',
    constraint_next=['LNER-A4-Tender'],
    liverytype=['LNER-Silver-Jubilee', 'LNER-Cornoation', 'LNER-Standard', 'WW2-Austerity', 'BR-Early', 'BR-Green'],
    blend='trains/Locomotives/lner-a4-apple.blend',
    upstream_dat='trains/lner-a4.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
