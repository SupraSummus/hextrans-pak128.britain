"""lnwr-bloomer-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-Bloomer-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1844,
    intro_month=12,
    retire_year=1866,
    retire_month=10,
    speed=115,
    length=3,
    weight=15,
    axles=3,
    brake_force=5,
    rolling_resistance=19,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    constraint_prev=['LNWR-Bloomer', 'LNWR-extra-large-bloomer', 'LNWR-small-bloomer', 'LNWR-Sharp-goods', 'LNWR-crewe-type', 'LNWR-mcconnell-large-single', 'lnwr-crewe-type-goods'],
    liverytype=['LNWR-Early', 'LNWR-Black'],
    blend='trains/Locomotives/lnwr-bloomer-tender-black.blend',
    upstream_dat='trains/lnwr-bloomer-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
