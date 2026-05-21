"""lms-fowler-3p."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-fowler-3p-br.blend'
_UPSTREAM_DAT = 'trains/lms-fowler-3p.dat'

SPECS = [
    Vehicle(
        name='LMS-Fowler-3P-Tank',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1930,
        intro_month=3,
        retire_year=1935,
        retire_month=12,
        speed=110,
        length=7,
        weight=67,
        axle_load=15,
        power=262,
        tractive_effort=98,
        payload=0,
        cost=2826214,
        runningcost=131,
        fixed_cost=26355,
        increase_maintenance_after_years=23,
        years_before_maintenance_max_reached=12,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        liverytype=['LMS-Standard', 'BR-Early'],
        upgrade=['LMS-Fowler-3P-Tank-Push-Pull'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-Fowler-3P-Tank-Push-Pull',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1930,
        intro_month=3,
        retire_year=1935,
        retire_month=12,
        speed=110,
        length=7,
        weight=67,
        axle_load=15,
        power=154,
        tractive_effort=98,
        payload=0,
        cost=3006214,
        runningcost=77,
        fixed_cost=26505,
        upgrade_price=49000,
        increase_maintenance_after_years=5,
        years_before_maintenance_max_reached=12,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
