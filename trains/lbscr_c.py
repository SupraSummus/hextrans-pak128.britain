"""lbscr-c."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lbscr-c-tender-goods-black.blend'
_UPSTREAM_DAT = 'trains/lbscr-c.dat'

SPECS = [
    Vehicle(
        name='LBSCR-C',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1871,
        intro_month=6,
        retire_year=1874,
        retire_month=12,
        speed=75,
        length=4,
        weight=39,
        axles=3,
        power=232,
        tractive_effort=82,
        brake_force=0,
        way_wear_factor=61425,
        payload=0,
        cost=7375000,
        runningcost=281,
        fixed_cost=30146,
        bidirectional=0,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LBSCR-C-tender'],
        liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LBSCR-C-tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1871,
        intro_month=6,
        retire_year=1874,
        retire_month=12,
        speed=145,
        length=3,
        weight=25,
        axles=3,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        bidirectional=0,
        can_lead_from_rear=0,
        constraint_prev=['LBSCR-C'],
        liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
