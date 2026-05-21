"""lms-ivatt-2p."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lms-ivatt-2p-br.blend'
_UPSTREAM_DAT = 'trains/lms-ivatt-2p.dat'

SPECS = [
    Vehicle(
        name='LMS-Ivatt-2P-Tank',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1946,
        intro_month=1,
        retire_year=1953,
        retire_month=7,
        speed=100,
        length=7,
        weight=64,
        axle_load=14,
        power=238,
        tractive_effort=77,
        payload=0,
        cost=3201213,
        runningcost=198,
        fixed_cost=26668,
        increase_maintenance_after_years=8,
        years_before_maintenance_max_reached=12,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        liverytype=['LMS-Standard', 'BR-Early'],
        upgrade=['LMS-Ivatt-2P-Tank-Push-Pull'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-Ivatt-2P-Tank-Push-Pull',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1946,
        intro_month=1,
        retire_year=1953,
        retire_month=7,
        speed=100,
        length=7,
        weight=72,
        axle_load=14,
        power=229,
        tractive_effort=77,
        payload=0,
        cost=3296213,
        runningcost=197,
        fixed_cost=26747,
        upgrade_price=50000,
        increase_maintenance_after_years=18,
        years_before_maintenance_max_reached=12,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
