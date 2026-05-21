"""stephenson-improved."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.locos-in-profile.co.uk/Early_Locomotives/Early_4.html
_BLEND = 'trains/Locomotives/stephenson-improved.blend'
_UPSTREAM_DAT = 'trains/stephenson-improved.dat'

SPECS = [
    Vehicle(
        name='stephenson-improved',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1816,
        intro_month=10,
        retire_year=1825,
        retire_month=12,
        speed=12,
        length=2,
        weight=7.2,
        axle_load=3,
        power=7,
        tractive_effort=1,
        brake_force=0,
        rolling_resistance=19,
        way_wear_factor=15300,
        payload=0,
        cost=1420000,
        runningcost=28,
        fixed_cost=17972,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['stephenson-improved-tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='stephenson-improved-tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1816,
        intro_month=10,
        retire_year=1825,
        retire_month=12,
        speed=12,
        length=2,
        weight=1,
        axles=2,
        brake_force=1,
        rolling_resistance=19,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['stephenson-improved'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
