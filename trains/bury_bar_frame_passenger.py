"""bury-bar-frame-passenger."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/Bury_Bar_Frame_locomotive
# http://www.steamlocomotive.com/locobase.php?country=Great_Britain&wheel=2-2-0&railroad=lb
# http://www.victorianweb.org/technology/railways/l6.html
_BLEND = 'trains/Locomotives/bury-bar-frame-passenger.blend'
_UPSTREAM_DAT = 'trains/bury-bar-frame-passenger.dat'

SPECS = [
    Vehicle(
        name='bury-bar-frame-passenger',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1837,
        intro_month=11,
        retire_year=1849,
        retire_month=1,
        speed=85,
        length=3,
        weight=8.5,
        axle_load=5,
        power=34,
        tractive_effort=4,
        brake_force=0,
        rolling_resistance=19,
        way_wear_factor=15888,
        payload=0,
        cost=5000000,
        runningcost=87,
        fixed_cost=22944,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['bury-bar-frame-tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='bury-bar-frame-tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1837,
        intro_month=11,
        retire_year=1849,
        retire_month=1,
        speed=85,
        length=2,
        weight=1,
        brake_force=1,
        rolling_resistance=19,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['bury-bar-frame-passenger', 'bury-bar-frame-goods'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
