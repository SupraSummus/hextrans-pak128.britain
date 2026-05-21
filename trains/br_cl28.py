"""br-cl28."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/br-cl28-blue.blend'
_UPSTREAM_DAT = 'trains/br-cl28.dat'

SPECS = [
    Vehicle(
        name='BR-Class28',
        waytype='track',
        copyright='Junna/Cake',
        freight='None',
        engine_type='diesel',
        intro_year=1958,
        intro_month=8,
        retire_year=1961,
        retire_month=2,
        speed=120,
        length=10,
        weight=98,
        axle_load=20,
        power=895,
        gear=50,
        tractive_effort=222,
        rolling_resistance=13,
        payload=0,
        cost=4500000,
        runningcost=896,
        fixed_cost=14688,
        increase_maintenance_after_years=12,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Diesel-heavy',
        sound='laurie-class-31.wav',
        constraint_prev=['BR-Class16', 'BR-Class21', 'BR-Class28', 'BR-Class29', 'BR-Class30', 'none'],
        liverytype=['BR-Early', 'BR-Blue'],
        upgrade=['BR-Class28-2'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='BR-Class28-2',
        waytype='track',
        copyright='Junna/Cake',
        freight='None',
        engine_type='diesel',
        intro_year=1968,
        intro_month=4,
        retire_year=1975,
        retire_month=7,
        speed=120,
        length=10,
        weight=98,
        axle_load=20,
        power=1230,
        gear=50,
        tractive_effort=275,
        rolling_resistance=13,
        payload=0,
        cost=4500000,
        runningcost=616,
        fixed_cost=13125,
        upgrade_price=1125000,
        increase_maintenance_after_years=12,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Diesel',
        sound='laurie-class-31.wav',
        constraint_prev=['BR-Class16', 'BR-Class21', 'BR-Class28', 'BR-Class29', 'BR-Class30', 'none'],
        liverytype=['BR-Early', 'BR-Blue'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
