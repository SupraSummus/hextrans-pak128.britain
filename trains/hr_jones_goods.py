"""hr-jones-goods."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='HR-Jones-Goods',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1894,
    intro_month=7,
    retire_year=1911,
    retire_month=8,
    speed=100,
    length=6,
    weight=57,
    axle_load=14,
    power=281,
    tractive_effort=109,
    payload=0,
    cost=4435200,
    runningcost=188,
    fixed_cost=27696,
    increase_maintenance_after_years=27,
    years_before_maintenance_max_reached=21,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['HR-Jones-Goods-Tender'],
    liverytype=['MR-Standard', 'LMS-Standard'],
    blend='trains/Locomotives/hr-jones-goods-lms.blend',
    upstream_dat='trains/hr-jones-goods.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
