"""sr-u-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/sr-u-class-austerity.blend'
_UPSTREAM_DAT = 'trains/sr-u-class.dat'

SPECS = [
    Vehicle(
        name='SR-U-Class',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1928,
        intro_month=8,
        retire_year=1940,
        retire_month=9,
        speed=120,
        length=6,
        weight=62,
        axle_load=18,
        power=359,
        tractive_effort=106,
        payload=0,
        cost=7521000,
        runningcost=201,
        fixed_cost=30268,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['SR-U-Class-Tender'],
        liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='SR-U-Class-Tender',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        intro_year=1928,
        intro_month=8,
        retire_year=1940,
        retire_month=9,
        speed=147,
        length=4,
        weight=45,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['SR-U-Class'],
        liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
