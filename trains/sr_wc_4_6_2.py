"""sr-wc-4-6-2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/sr-wc-4-6-2.blend'
_UPSTREAM_DAT = 'trains/sr-wc-4-6-2.dat'

SPECS = [
    Vehicle(
        name='SR-WestCountry_4-6-2',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1945,
        intro_month=5,
        retire_year=1951,
        retire_month=5,
        speed=155,
        length=7,
        weight=87.4,
        axle_load=19,
        power=468,
        tractive_effort=137,
        way_wear_factor=109250,
        payload=0,
        cost=9216500,
        runningcost=320,
        fixed_cost=31680,
        increase_maintenance_after_years=7,
        years_before_maintenance_max_reached=14,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['SR-WestCountry_4-6-2-tender'],
        liverytype=['SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        upgrade=['SR-WestCountryRebuilt_4-6-2'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='SR-WestCountry_4-6-2-tender',
        waytype='track',
        copyright='Kieron/jamespetts',
        freight='None',
        intro_year=1945,
        intro_month=5,
        retire_year=1951,
        retire_month=5,
        speed=160,
        length=4,
        weight=42.7,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=7,
        years_before_maintenance_max_reached=14,
        constraint_prev=['SR-WestCountry_4-6-2'],
        liverytype=['SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        upgrade=['BR-7MT-Tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
