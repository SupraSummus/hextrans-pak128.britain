"""lms-2p."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-2p-tender.blend'
_UPSTREAM_DAT = 'trains/lms-2p.dat'

SPECS = [
    Vehicle(
        name='LMS-2P',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1928,
        intro_month=1,
        retire_year=1932,
        retire_month=7,
        speed=140,
        length=5,
        weight=55,
        axle_load=16,
        power=228,
        tractive_effort=79,
        payload=0,
        cost=7025000,
        runningcost=171,
        fixed_cost=29854,
        increase_maintenance_after_years=23,
        years_before_maintenance_max_reached=18,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LMS-2P-Tender'],
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-2P-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1928,
        intro_month=1,
        retire_year=1932,
        retire_month=7,
        speed=140,
        length=4,
        weight=43,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=23,
        constraint_prev=['LMS-2P'],
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
