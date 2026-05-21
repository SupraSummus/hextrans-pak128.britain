"""lbscr-k."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lbscr-k-austerity.blend'
_UPSTREAM_DAT = 'trains/lbscr-k.dat'

SPECS = [
    Vehicle(
        name='LBSCR-K',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1913,
        intro_month=9,
        retire_year=1921,
        retire_month=3,
        speed=115,
        length=6,
        weight=64,
        axle_load=18,
        power=386,
        tractive_effort=118,
        payload=0,
        cost=6852500,
        runningcost=149,
        fixed_cost=29710,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LBSCR-K-Tender'],
        liverytype=['LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LBSCR-K-Tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        intro_year=1913,
        intro_month=9,
        retire_year=1921,
        retire_month=3,
        speed=123,
        length=4,
        weight=32,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['LBSCR-K'],
        liverytype=['LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
