"""lms-jinty."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-jinty-black.blend'
_UPSTREAM_DAT = 'trains/lms-jinty.dat'

SPECS = [
    Vehicle(
        name='LMS-3F-Jinty',
        waytype='track',
        copyright='Kieron',
        freight='None',
        engine_type='steam',
        intro_year=1924,
        intro_month=6,
        retire_year=1953,
        retire_month=11,
        speed=90,
        length=5,
        weight=50.3,
        axles=3,
        power=208,
        tractive_effort=93,
        way_wear_factor=79223,
        payload=0,
        cost=1584000,
        runningcost=122,
        fixed_cost=25320,
        upgrade_price=55000,
        increase_maintenance_after_years=9,
        years_before_maintenance_max_reached=12,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        liverytype=['LMS-Standard', 'BR-Early'],
        upgrade=['LMS-3F-Jinty-Push-Pull'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-3F-Jinty-Push-Pull',
        waytype='track',
        copyright='Kieron',
        freight='None',
        engine_type='steam',
        intro_year=1924,
        intro_month=6,
        retire_year=1953,
        retire_month=11,
        speed=90,
        length=5,
        weight=50.3,
        axles=3,
        power=208,
        tractive_effort=93,
        way_wear_factor=79223,
        payload=0,
        cost=1584000,
        runningcost=69,
        fixed_cost=25320,
        upgrade_price=55000,
        increase_maintenance_after_years=9,
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
