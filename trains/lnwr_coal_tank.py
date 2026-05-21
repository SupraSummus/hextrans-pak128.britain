"""lnwr-coal-tank."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.lnwrs.org.uk/GoodsLocos/Loco05.php
SPEC = Vehicle(
    name='LNWR-coal-tank',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1881,
    intro_month=3,
    retire_year=1896,
    retire_month=3,
    speed=82,
    length=6,
    weight=44,
    axles=3,
    power=206,
    tractive_effort=74,
    brake_force=13,
    way_wear_factor=69300,
    payload=0,
    cost=4000000,
    runningcost=118,
    fixed_cost=27333,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LNWR-Black', 'LMS-Standard', 'BR-Early'],
    blend='trains/Locomotives/lnwr-coal-tank-lms.blend',
    upstream_dat='trains/lnwr-coal-tank.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
