"""mr-1000-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='MR-1000-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    intro_year=1901,
    intro_month=12,
    retire_year=1924,
    retire_month=2,
    speed=145,
    length=4,
    weight=39,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    constraint_prev=['MR-2631', 'MR-1000', 'MR-1000-superheated'],
    liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/mr-1000-tender-br-unlined.blend',
    upstream_dat='trains/mr-1000-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
