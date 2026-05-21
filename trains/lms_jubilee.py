"""lms-jubilee."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-jubilee-wartime.blend'
_UPSTREAM_DAT = 'trains/lms-jubilee.dat'

SPECS = [
    Vehicle(
        name='LMS-Jubilee',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1934,
        intro_month=11,
        retire_year=1945,
        retire_month=12,
        speed=150,
        length=7,
        weight=81,
        axle_load=20,
        power=489,
        tractive_effort=119,
        way_wear_factor=11375,
        payload=0,
        cost=6689000,
        runningcost=272,
        fixed_cost=29574,
        increase_maintenance_after_years=15,
        years_before_maintenance_max_reached=11,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['LMS-Jubilee-Tender'],
        liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-Jubilee-Tender',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        intro_year=1934,
        intro_month=11,
        retire_year=1945,
        retire_month=12,
        speed=150,
        length=4,
        weight=55,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=15,
        years_before_maintenance_max_reached=11,
        constraint_prev=['LMS-Jubilee'],
        liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
