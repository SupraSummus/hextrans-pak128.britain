"""lbscr-h1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lbscr-h1-tender-austerity.blend'
_UPSTREAM_DAT = 'trains/lbscr-h1.dat'

SPECS = [
    Vehicle(
        name='LBSCR-H1',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1905,
        intro_month=12,
        retire_year=1911,
        retire_month=6,
        speed=150,
        length=6,
        weight=68,
        axle_load=19,
        power=360,
        tractive_effort=85,
        payload=0,
        cost=8346250,
        runningcost=163,
        fixed_cost=46955,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['LBSCR-H1-Tender'],
        liverytype=['LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LBSCR-H1-Tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        intro_year=1905,
        intro_month=12,
        retire_year=1916,
        retire_month=10,
        speed=150,
        length=4,
        weight=43,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=28,
        years_before_maintenance_max_reached=25,
        constraint_prev=['LBSCR-H1', 'LBSCR-H2'],
        liverytype=['LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
