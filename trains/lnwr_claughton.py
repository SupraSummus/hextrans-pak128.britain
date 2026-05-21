"""lnwr-claughton."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lnwr-claughton-lms.blend'
_UPSTREAM_DAT = 'trains/lnwr-claughton.dat'

SPECS = [
    Vehicle(
        name='LNWR-Claughton',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1913,
        intro_month=8,
        retire_year=1921,
        retire_month=12,
        speed=152,
        length=6,
        weight=79,
        axle_load=20,
        power=441,
        tractive_effort=120,
        way_wear_factor=103688,
        payload=0,
        cost=13200000,
        runningcost=190,
        fixed_cost=51000,
        increase_maintenance_after_years=15,
        years_before_maintenance_max_reached=21,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['LNWR-Claughton-tender'],
        liverytype=['LNWR-Black', 'LMS-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNWR-Claughton-tender',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        intro_year=1913,
        intro_month=8,
        retire_year=1921,
        retire_month=12,
        speed=145,
        length=4,
        weight=40,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=15,
        years_before_maintenance_max_reached=21,
        constraint_prev=['LNWR-Claughton'],
        liverytype=['LNWR-Black', 'LMS-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
