"""lms-royal-scot."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-royal-scot-wartime.blend'
_UPSTREAM_DAT = 'trains/lms-royal-scot.dat'

SPECS = [
    Vehicle(
        name='LMS-royal-scot',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1927,
        intro_month=4,
        retire_year=1933,
        retire_month=6,
        speed=155,
        length=7,
        weight=86.3,
        axle_load=20,
        power=612,
        tractive_effort=148,
        way_wear_factor=118663,
        payload=0,
        cost=6975000,
        runningcost=392,
        fixed_cost=54531,
        increase_maintenance_after_years=17,
        years_before_maintenance_max_reached=12,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['LMS-royal-scot-tender'],
        liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
        upgrade=['LMS-rebuilt-royal-scot'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-royal-scot-tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1927,
        intro_month=4,
        retire_year=1933,
        retire_month=6,
        speed=155,
        length=4,
        weight=43,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=14,
        years_before_maintenance_max_reached=11,
        constraint_prev=['LMS-royal-scot'],
        liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
        upgrade=['LMS-rebuilt-royal-scot-tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
