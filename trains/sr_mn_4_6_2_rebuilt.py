"""sr-mn-4-6-2-rebuilt."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SR-MerchantNavyRebuilt_4-6-2',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1956,
    intro_month=5,
    retire_year=1959,
    retire_month=12,
    speed=160,
    length=8,
    weight=99.5,
    axle_load=21,
    power=690,
    tractive_effort=149,
    way_wear_factor=136813,
    payload=0,
    cost=13522500,
    runningcost=514,
    fixed_cost=68172,
    upgrade_price=6900000,
    increase_maintenance_after_years=4,
    years_before_maintenance_max_reached=10,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['BR-7MT-Tender'],
    blend='trains/Locomotives/sr-mn-4-6-2-rebuilt.blend',
    upstream_dat='trains/sr-mn-4-6-2-rebuilt.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
