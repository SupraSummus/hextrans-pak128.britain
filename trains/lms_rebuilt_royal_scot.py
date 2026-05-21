"""lms-rebuilt-royal-scot."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-rebuilt-royal-scot-wartime.blend'
_UPSTREAM_DAT = 'trains/lms-rebuilt-royal-scot.dat'

SPECS = [
    Vehicle(
        name='LMS-rebuilt-royal-scot',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1943,
        intro_month=2,
        retire_year=1955,
        retire_month=10,
        speed=155,
        length=7,
        weight=86,
        axle_load=20,
        power=403,
        tractive_effort=148,
        payload=0,
        cost=7000000,
        runningcost=302,
        fixed_cost=29833,
        upgrade_price=5022000,
        increase_maintenance_after_years=5,
        years_before_maintenance_max_reached=15,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['LMS-rebuilt-royal-scot-tender'],
        liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-rebuilt-royal-scot-tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1943,
        intro_month=2,
        retire_year=1955,
        retire_month=10,
        speed=155,
        length=4,
        weight=55,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=5,
        years_before_maintenance_max_reached=15,
        constraint_prev=['LMS-rebuilt-royal-scot'],
        liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
