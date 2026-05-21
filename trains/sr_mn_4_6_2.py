"""sr-mn-4-6-2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/sr-mn-4-6-2.blend'
_UPSTREAM_DAT = 'trains/sr-mn-4-6-2.dat'

SPECS = [
    Vehicle(
        name='SR-MerchantNavy_4-6-2',
        waytype='track',
        copyright='Kieron/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1941,
        intro_month=2,
        retire_year=1949,
        retire_month=4,
        speed=160,
        length=7,
        weight=96.3,
        axle_load=21,
        power=649,
        tractive_effort=167,
        way_wear_factor=120375,
        payload=0,
        cost=10298000,
        runningcost=460,
        fixed_cost=61454,
        increase_maintenance_after_years=7,
        years_before_maintenance_max_reached=9,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['SR-MerchantNavy_4-6-2Tender'],
        liverytype=['SR-Malachite-Green', 'WW2-Austerity', 'BR-Early', 'BR-Green'],
        upgrade=['SR-MerchantNavyRebuilt_4-6-2'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='SR-MerchantNavy_4-6-2Tender',
        waytype='track',
        copyright='Kieron/jamespetts',
        freight='None',
        intro_year=1941,
        intro_month=2,
        retire_year=1949,
        retire_month=4,
        speed=160,
        length=4,
        weight=47,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=7,
        years_before_maintenance_max_reached=9,
        constraint_prev=['SR-MerchantNavy_4-6-2'],
        liverytype=['SR-Malachite-Green', 'WW2-Austerity', 'BR-Early', 'BR-Green'],
        upgrade=['BR-7MT-Tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
