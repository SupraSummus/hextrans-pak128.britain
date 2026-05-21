"""lancashire-witch."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.steamlocomotive.com/locobase.php?country=Great_Britain&wheel=0-4-0&railroad=bl
# See also Ahrons p. 9
_BLEND = 'trains/Locomotives/lancashire-witch-tender.blend'
_UPSTREAM_DAT = 'trains/lancashire-witch.dat'

SPECS = [
    Vehicle(
        name='lancashire-witch',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1828,
        intro_month=6,
        retire_year=1834,
        retire_month=5,
        speed=25,
        length=2,
        weight=7.0,
        axle_load=4,
        power=20,
        tractive_effort=2,
        brake_force=0,
        rolling_resistance=19,
        way_wear_factor=15313,
        payload=0,
        cost=1000000,
        runningcost=80,
        fixed_cost=17389,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['lancashire-witch-tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='lancashire-witch-tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1828,
        intro_month=6,
        retire_year=1834,
        retire_month=5,
        speed=25,
        length=2,
        weight=1,
        axles=2,
        brake_force=1,
        rolling_resistance=19,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['lancashire-witch'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
