"""secr-n-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/secr-n-class-ww1-austerity.blend'
_UPSTREAM_DAT = 'trains/secr-n-class.dat'

SPECS = [
    Vehicle(
        name='SECR-N-Class',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1917,
        intro_month=7,
        retire_year=1934,
        retire_month=11,
        speed=110,
        length=6,
        weight=61,
        axle_load=17,
        power=368,
        tractive_effort=116,
        way_wear_factor=100800,
        payload=0,
        cost=7400000,
        runningcost=200,
        fixed_cost=30167,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['SECR-N-Class-Tender'],
        liverytype=['WW1-Austerity', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='SECR-N-Class-Tender',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        intro_year=1917,
        intro_month=7,
        retire_year=1934,
        retire_month=11,
        speed=110,
        length=4,
        weight=45,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['SECR-N-Class', 'SECR-N1-Class'],
        liverytype=['WW1-Austerity', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
