"""mr-2000."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/mr-2000-superheated-lms.blend'
_UPSTREAM_DAT = 'trains/mr-2000.dat'

SPECS = [
    Vehicle(
        name='MR-2000',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1907,
        intro_month=6,
        retire_year=1918,
        retire_month=8,
        speed=85,
        length=7,
        weight=73.6,
        axle_load=18,
        power=264,
        tractive_effort=83,
        way_wear_factor=114795,
        payload=0,
        cost=3520000,
        runningcost=117,
        fixed_cost=26933,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        liverytype=['MR-Standard', 'LMS-Standard'],
        upgrade=['MR-2000-superheated'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='MR-2000-superheated',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1920,
        intro_month=3,
        retire_year=1933,
        retire_month=4,
        speed=85,
        length=7,
        weight=76,
        axle_load=18,
        power=298,
        tractive_effort=88,
        way_wear_factor=119700,
        payload=0,
        cost=3659000,
        runningcost=168,
        fixed_cost=27049,
        upgrade_price=1750000,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        liverytype=['MR-Standard', 'LMS-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
