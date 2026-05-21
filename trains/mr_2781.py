"""mr-2781."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/mr-2781-lms.blend'
_UPSTREAM_DAT = 'trains/mr-2781.dat'

SPECS = [
    Vehicle(
        name='MR-2781',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1900,
        intro_month=3,
        retire_year=1905,
        retire_month=8,
        speed=147,
        length=6,
        weight=56,
        axle_load=18,
        power=316,
        tractive_effort=89,
        payload=0,
        cost=6841000,
        runningcost=136,
        fixed_cost=45701,
        increase_maintenance_after_years=16,
        years_before_maintenance_max_reached=25,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['MR-2781-Tender'],
        liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='MR-2781-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1890,
        intro_month=4,
        retire_year=1911,
        retire_month=6,
        speed=135,
        length=4,
        weight=37,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=16,
        constraint_prev=['MR-2781', 'MR-1873', 'MR-2736'],
        liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
