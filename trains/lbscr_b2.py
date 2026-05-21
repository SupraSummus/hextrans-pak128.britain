"""lbscr-b2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lbscr-b2-olive.blend'
_UPSTREAM_DAT = 'trains/lbscr-b2.dat'

SPECS = [
    Vehicle(
        name='LBSCR-B2',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1895,
        intro_month=6,
        retire_year=1898,
        retire_month=1,
        speed=130,
        length=5,
        weight=43,
        axle_load=15,
        power=241,
        tractive_effort=63,
        payload=0,
        cost=5900000,
        runningcost=154,
        fixed_cost=28917,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LBSCR-B2-tender'],
        liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green'],
        upgrade=['LBSCR-B2x'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LBSCR-B2-tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1895,
        intro_month=6,
        retire_year=1898,
        retire_month=1,
        speed=135,
        length=4,
        weight=32,
        axles=3,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['LBSCR-B2', 'LBSCR-B2x'],
        liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
