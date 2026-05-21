"""lnwr-bloomer."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Note: the LNWR black livery version is the unmodified version
# (which did exist in black: see http://www.lnwrs.org.uk/PassLocos/P001L2.jpg).
# The modified versions with full cabs had 120lb boilers - consider adding
# these later.
SPEC = Vehicle(
    name='LNWR-Bloomer',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1851,
    intro_month=5,
    retire_year=1862,
    retire_month=6,
    speed=115,
    length=4,
    weight=30,
    axle_load=12,
    power=160,
    tractive_effort=26,
    brake_force=0,
    rolling_resistance=19,
    payload=0,
    cost=16598400,
    runningcost=258,
    fixed_cost=37832,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LNWR-Bloomer-Tender'],
    liverytype=['LNWR-Early', 'LNWR-Black'],
    blend='trains/Locomotives/lnwr-bloomer-tender-black.blend',
    upstream_dat='trains/lnwr-bloomer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
