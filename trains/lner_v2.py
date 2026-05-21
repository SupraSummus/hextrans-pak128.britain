"""lner-v2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-V2',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1936,
    intro_month=6,
    retire_year=1944,
    retire_month=10,
    speed=147,
    length=7,
    weight=93,
    axle_load=22,
    power=670,
    tractive_effort=150,
    way_wear_factor=127875,
    payload=0,
    cost=6585600,
    runningcost=384,
    fixed_cost=53720,
    increase_maintenance_after_years=16,
    years_before_maintenance_max_reached=9,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['LNER-V2-Tender'],
    liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lner-v2-br.blend',
    upstream_dat='trains/lner-v2.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
