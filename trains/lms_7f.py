"""lms-7f."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-7f.blend'
_UPSTREAM_DAT = 'trains/lms-7f.dat'

SPECS = [
    Vehicle(
        name='LMS-7F',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1929,
        intro_month=4,
        retire_year=1935,
        retire_month=3,
        speed=95,
        length=6,
        weight=62,
        axles=4,
        power=372,
        tractive_effort=132,
        payload=0,
        cost=4286000,
        runningcost=201,
        fixed_cost=27572,
        increase_maintenance_after_years=23,
        years_before_maintenance_max_reached=12,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LMS-7F-Tender'],
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-7F-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1929,
        intro_month=4,
        retire_year=1935,
        retire_month=3,
        speed=95,
        length=4,
        weight=42,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=23,
        years_before_maintenance_max_reached=12,
        constraint_prev=['LMS-7F'],
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
