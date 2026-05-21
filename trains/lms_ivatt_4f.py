"""lms-ivatt-4f."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-ivatt-4f-tender.blend'
_UPSTREAM_DAT = 'trains/lms-ivatt-4f.dat'

SPECS = [
    Vehicle(
        name='LMS-Ivatt-4F',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1947,
        intro_month=2,
        retire_year=1952,
        retire_month=12,
        speed=115,
        length=6,
        weight=60,
        axle_load=17,
        power=320,
        tractive_effort=108,
        payload=0,
        cost=4500000,
        runningcost=271,
        fixed_cost=27750,
        increase_maintenance_after_years=12,
        years_before_maintenance_max_reached=11,
        bidirectional=0,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LMS-Ivatt-4F-Tender'],
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-Ivatt-4F-Tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        intro_year=1947,
        intro_month=2,
        retire_year=1952,
        retire_month=12,
        speed=115,
        length=4,
        weight=43,
        axle_load=17,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=12,
        years_before_maintenance_max_reached=11,
        constraint_prev=['LMS-Ivatt-4F'],
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
