"""lnwr-problem."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNWR-Problem',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1859,
    intro_month=11,
    retire_year=1866,
    retire_month=5,
    speed=117,
    length=4,
    weight=27,
    axle_load=11,
    power=173,
    tractive_effort=27,
    brake_force=0,
    rolling_resistance=19,
    payload=0,
    cost=15206400,
    runningcost=279,
    fixed_cost=36672,
    increase_maintenance_after_years=40,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-Problem-Tender'],
    liverytype=['LNWR-Early', 'LNWR-Black'],
    blend='trains/Locomotives/lnwr-problem-black.blend',
    upstream_dat='trains/lnwr-problem.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
