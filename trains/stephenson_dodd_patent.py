"""stephenson-dodd-patent."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.locos-in-profile.co.uk/Early_Locomotives/Early_4.html
_BLEND = 'trains/Locomotives/stephenson-dodd-patent.blend'
_UPSTREAM_DAT = 'trains/stephenson-dodd-patent.dat'

SPECS = [
    Vehicle(
        name='stephenson-dodd-patent',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1815,
        intro_month=2,
        retire_year=1817,
        retire_month=9,
        speed=8,
        length=2,
        weight=7.1,
        axle_load=3,
        power=7,
        tractive_effort=1,
        brake_force=0,
        rolling_resistance=19,
        way_wear_factor=15975,
        payload=0,
        cost=1400000,
        runningcost=28,
        fixed_cost=17944,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['stephenson-dodd-patent-tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='stephenson-dodd-patent-tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1815,
        intro_month=2,
        retire_year=1817,
        retire_month=9,
        speed=8,
        length=2,
        weight=1,
        axles=2,
        brake_force=1,
        rolling_resistance=19,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['stephenson-dodd-patent'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
