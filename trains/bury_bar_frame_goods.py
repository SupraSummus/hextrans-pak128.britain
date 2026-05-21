"""bury-bar-frame-goods."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/Bury_Bar_Frame_locomotive
# http://www.steamlocomotive.com/locobase.php?country=Great_Britain&wheel=2-2-0&railroad=lb
# http://www.victorianweb.org/technology/railways/l6.html
SPEC = Vehicle(
    name='bury-bar-frame-goods',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1837,
    intro_month=11,
    retire_year=1849,
    retire_month=1,
    speed=56,
    length=3,
    weight=8.7,
    axles=2,
    power=34,
    tractive_effort=5,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=18053,
    payload=0,
    cost=5050000,
    runningcost=87,
    fixed_cost=23014,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['bury-bar-frame-tender'],
    blend='trains/Locomotives/bury-bar-frame-goods.blend',
    upstream_dat='trains/bury-bar-frame-goods.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
