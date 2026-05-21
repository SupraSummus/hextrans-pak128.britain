"""stephenson-long-boiler-goods."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Ahrons p. 58
_BLEND = 'trains/Locomotives/stephenson-long-boiler-goods-mr-dark.blend'
_UPSTREAM_DAT = 'trains/stephenson-long-boiler-goods.dat'

SPECS = [
    Vehicle(
        name='stephenson-long-boiler-goods',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1843,
        intro_month=5,
        retire_year=1855,
        retire_month=7,
        speed=56,
        length=4,
        weight=21.5,
        axle_load=8,
        power=70,
        tractive_effort=22,
        brake_force=0,
        rolling_resistance=19,
        payload=0,
        cost=14800000,
        runningcost=117,
        fixed_cost=44556,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['stephenson-long-boiler-goods-tender'],
        liverytype=['MR-Early', 'MR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='stephenson-long-boiler-goods-tender',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1843,
        intro_month=5,
        retire_year=1855,
        retire_month=7,
        speed=56,
        length=3,
        weight=14,
        brake_force=3,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['stephenson-long-boiler-goods'],
        liverytype=['MR-Early', 'MR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
