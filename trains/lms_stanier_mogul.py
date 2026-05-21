"""lms-stanier-mogul."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-stanier-mogul-br.blend'
_UPSTREAM_DAT = 'trains/lms-stanier-mogul.dat'

SPECS = [
    Vehicle(
        name='LMS-Stanier-Mogul',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1933,
        intro_month=8,
        retire_year=1947,
        retire_month=2,
        speed=125,
        length=7,
        weight=70,
        axle_load=20,
        power=409,
        tractive_effort=117,
        payload=0,
        cost=4610000,
        runningcost=234,
        fixed_cost=27842,
        increase_maintenance_after_years=18,
        years_before_maintenance_max_reached=10,
        bidirectional=0,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LMS-Stanier-Mogul-Tender'],
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-Stanier-Mogul-Tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        intro_year=1933,
        intro_month=8,
        retire_year=1947,
        retire_month=2,
        speed=125,
        length=4,
        weight=43,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=18,
        years_before_maintenance_max_reached=10,
        constraint_prev=['LMS-Stanier-Mogul'],
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
