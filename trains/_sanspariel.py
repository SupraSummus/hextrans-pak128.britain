"""sanspariel."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.steamlocomotive.com/locobase.php?country=Great_Britain&wheel=0-4-0&railroad=lm
# See also Ahrons pp. 13-4
_BLEND = 'trains/Locomotives/sanspariel.blend'
_UPSTREAM_DAT = 'trains/sanspariel.dat'

SPECS = [
    Vehicle(
        name='sanspariel',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1829,
        intro_month=9,
        retire_year=1833,
        retire_month=5,
        speed=30,
        length=2,
        weight=4.8,
        axle_load=2,
        power=19,
        tractive_effort=4,
        brake_force=0,
        rolling_resistance=19,
        way_wear_factor=10614,
        payload=0,
        cost=1022500,
        runningcost=64,
        fixed_cost=17420,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['sanspariel-tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='sanspariel-tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1829,
        intro_month=9,
        retire_year=1833,
        retire_month=5,
        speed=30,
        length=2,
        weight=1,
        brake_force=1,
        rolling_resistance=19,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['sanspariel'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
