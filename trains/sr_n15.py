"""sr-n15."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SR-N15',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1922,
    intro_month=4,
    retire_year=1926,
    retire_month=11,
    speed=142,
    length=6,
    weight=81,
    axle_load=19,
    power=430,
    tractive_effort=106,
    payload=0,
    cost=11491200,
    runningcost=249,
    fixed_cost=49576,
    upgrade_price=750000,
    increase_maintenance_after_years=27,
    years_before_maintenance_max_reached=12,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['SR-N15-Tender'],
    liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/sr-n15-tender-austerity.blend',
    upstream_dat='trains/sr-n15.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
