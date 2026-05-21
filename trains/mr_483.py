"""mr-483."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/mr-483-tender-lms.blend'
_UPSTREAM_DAT = 'trains/mr-483.dat'

SPECS = [
    Vehicle(
        name='MR-483',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1910,
        intro_month=2,
        retire_year=1928,
        retire_month=1,
        speed=142,
        length=5,
        weight=54.2,
        axle_load=17,
        power=278,
        tractive_effort=78,
        payload=0,
        cost=6841000,
        runningcost=120,
        fixed_cost=29701,
        upgrade_price=3420500,
        increase_maintenance_after_years=16,
        years_before_maintenance_max_reached=25,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['MR-483-Tender'],
        liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='MR-483-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1890,
        intro_month=4,
        retire_year=1928,
        retire_month=1,
        speed=135,
        length=4,
        weight=37,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=16,
        constraint_prev=['MR-483', 'MR-1873', 'MR-2736'],
        liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
