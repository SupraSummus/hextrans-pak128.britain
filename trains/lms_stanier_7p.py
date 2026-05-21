"""lms-stanier-7p."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-stanier-0-4-4T-br.blend'
_UPSTREAM_DAT = 'trains/lms-stanier-7p.dat'

SPECS = [
    Vehicle(
        name='LMS-Stanier-7P',
        waytype='track',
        copyright='Kieron',
        freight='None',
        engine_type='steam',
        intro_year=1937,
        intro_month=6,
        retire_year=1946,
        retire_month=2,
        speed=160,
        length=9,
        weight=109.8,
        axle_load=22,
        power=777,
        tractive_effort=180,
        way_wear_factor=144113,
        payload=0,
        cost=10458000,
        runningcost=436,
        fixed_cost=48715,
        increase_maintenance_after_years=14,
        years_before_maintenance_max_reached=10,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['LMS-Stanier-7P-Tender'],
        liverytype=['LMS-Standard', 'LMS-Blue'],
        upgrade=['LMS-Stanier-7P-non-streamlined'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-Stanier-7P-non-streamlined',
        waytype='track',
        copyright='Kieron',
        freight='None',
        engine_type='steam',
        intro_year=1946,
        intro_month=2,
        retire_year=1954,
        retire_month=4,
        speed=160,
        length=8,
        weight=106.9,
        axle_load=22,
        power=773,
        tractive_effort=180,
        way_wear_factor=140306,
        payload=0,
        cost=10020000,
        runningcost=604,
        fixed_cost=60875,
        upgrade_price=10000,
        increase_maintenance_after_years=7,
        years_before_maintenance_max_reached=10,
        smoke='Steam',
        constraint_next=['LMS-Princess-Royal-Tender'],
        liverytype=['LMS-Standard', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
