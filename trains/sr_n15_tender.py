"""sr-n15-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SR-N15-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    intro_year=1922,
    intro_month=4,
    retire_year=1926,
    retire_month=11,
    speed=145,
    length=4,
    weight=57,
    axles=4,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=27,
    years_before_maintenance_max_reached=12,
    constraint_prev=['SR-N15'],
    liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/sr-n15-tender-austerity.blend',
    upstream_dat='trains/sr-n15-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
