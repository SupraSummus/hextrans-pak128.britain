"""gnr-c1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/gnr-c1-lner.blend'
_UPSTREAM_DAT = 'trains/gnr-c1.dat'

SPECS = [
    Vehicle(
        name='GNR-C1',
        waytype='track',
        copyright='Kieron',
        freight='None',
        engine_type='steam',
        intro_year=1902,
        intro_month=12,
        retire_year=1910,
        retire_month=3,
        speed=150,
        length=6,
        weight=70.7,
        axle_load=18,
        power=361,
        tractive_effort=70,
        payload=0,
        cost=8346250,
        runningcost=162,
        fixed_cost=46955,
        increase_maintenance_after_years=28,
        years_before_maintenance_max_reached=25,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['GNR-C1-Tender'],
        liverytype=['GNR-Standard', 'LNER-Standard'],
        upgrade=['GNR-C1-superheated'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='GNR-C1-superheated',
        waytype='track',
        copyright='Kieron',
        freight='None',
        engine_type='steam',
        intro_year=1910,
        intro_month=3,
        retire_year=1924,
        retire_month=4,
        speed=150,
        length=6,
        weight=70.7,
        axle_load=20,
        power=434,
        tractive_effort=77,
        payload=0,
        cost=8646250,
        runningcost=172,
        fixed_cost=47205,
        upgrade_price=576417,
        increase_maintenance_after_years=28,
        years_before_maintenance_max_reached=25,
        smoke='Steam',
        constraint_next=['GNR-C1-Tender'],
        liverytype=['GNR-Standard', 'LNER-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
