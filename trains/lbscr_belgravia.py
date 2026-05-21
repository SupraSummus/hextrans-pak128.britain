"""lbscr-belgravia."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lbscr-belgravia-tender-umber.blend'
_UPSTREAM_DAT = 'trains/lbscr-belgravia.dat'

SPECS = [
    Vehicle(
        name='LBSCR-Belgravia',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1872,
        intro_month=2,
        retire_year=1876,
        retire_month=11,
        speed=127,
        length=4,
        weight=41.9,
        axle_load=15,
        power=236,
        tractive_effort=44,
        payload=0,
        cost=12375000,
        runningcost=267,
        fixed_cost=34313,
        increase_maintenance_after_years=40,
        years_before_maintenance_max_reached=35,
        bidirectional=0,
        can_lead_from_rear=0,
        smoke='Steam',
        constraint_next=['LBSCR-Belgravia-tender'],
        liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LBSCR-Belgravia-tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1872,
        intro_month=2,
        retire_year=1883,
        retire_month=9,
        speed=145,
        length=2,
        weight=25,
        axles=3,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        bidirectional=0,
        can_lead_from_rear=0,
        constraint_prev=['LBSCR-Belgravia', 'LBSCR-G', 'LBSCR-Richmond', 'LBSCR-D2'],
        liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
