"""royal-george."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Ahrons, p. 5 and
# http://www.steamlocomotive.com/locobase.php?country=Great_Britain&wheel=0-6-0&railroad=sd
# https://upload.wikimedia.org/wikipedia/commons/1/10/Hackworth%27s_%27Royal_George%27%2C_1827_%28British_Railway_Locomotives_1803-1853%29.jpg
_BLEND = 'trains/Locomotives/royal-george.blend'
_UPSTREAM_DAT = 'trains/royal-george.dat'

SPECS = [
    Vehicle(
        name='royal-george',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1827,
        intro_month=9,
        retire_year=1833,
        retire_month=1,
        speed=20,
        length=3,
        weight=10.0,
        axles=3,
        power=11,
        tractive_effort=6,
        brake_force=0,
        rolling_resistance=20,
        payload=0,
        cost=6200000,
        runningcost=46,
        fixed_cost=24611,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['royal-george-tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='royal-george-tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1827,
        intro_month=9,
        retire_year=1833,
        retire_month=1,
        speed=20,
        length=2,
        weight=1,
        brake_force=1,
        rolling_resistance=19,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['royal-george'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
