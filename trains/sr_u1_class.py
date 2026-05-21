"""sr-u1-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/sr-u1-class-austerity.blend'
_UPSTREAM_DAT = 'trains/sr-u1-class.dat'

SPECS = [
    Vehicle(
        name='SR-U1-Class',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1928,
        intro_month=3,
        retire_year=1940,
        retire_month=9,
        speed=117,
        length=6,
        weight=65,
        axle_load=18,
        power=358,
        tractive_effort=113,
        way_wear_factor=89375,
        payload=0,
        cost=8075000,
        runningcost=199,
        fixed_cost=30729,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['SR-U1-Class-Tender'],
        liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='SR-U1-Class-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1928,
        intro_month=3,
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
        constraint_prev=['SR-U1-Class'],
        liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
