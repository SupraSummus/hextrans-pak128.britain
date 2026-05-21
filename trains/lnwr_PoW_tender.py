"""lnwr-PoW-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-PrinceOfWales-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    intro_year=1897,
    intro_month=5,
    retire_year=1924,
    retire_month=5,
    speed=150,
    length=4,
    weight=35,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=16,
    years_before_maintenance_max_reached=22,
    constraint_prev=['LNWR-PrinceOfWales', 'LNWR-Precursor', 'LNWR-George-V', 'LNWR-Jubilee', 'LNWR-Alfred-the-Great', 'LNWR-Experiment', 'LNWR-19in-express-goods'],
    liverytype=['LNWR-Black', 'LMS-Standard'],
    blend='trains/Locomotives/lnwr-PoW-tender-lms-black.blend',
    upstream_dat='trains/lnwr-PoW-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
