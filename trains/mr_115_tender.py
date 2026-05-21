"""mr-115-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-Spinner-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    intro_year=1896,
    intro_month=2,
    retire_year=1904,
    retire_month=10,
    speed=140,
    length=4,
    weight=34,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=30,
    years_before_maintenance_max_reached=20,
    constraint_prev=['MR-Spinner', 'MR-2601'],
    blend='trains/Locomotives/mr-115-class.blend',
    upstream_dat='trains/mr-115-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
