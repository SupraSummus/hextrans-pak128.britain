"""sr-lord-nelson."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/sr-lord-nelson-tender-austerity.blend'
_UPSTREAM_DAT = 'trains/sr-lord-nelson.dat'

SPECS = [
    Vehicle(
        name='SR-Lord-Nelson',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1926,
        intro_month=8,
        retire_year=1940,
        retire_month=3,
        speed=145,
        length=7,
        weight=83,
        axle_load=21,
        power=500,
        tractive_effort=149,
        way_wear_factor=108938,
        payload=0,
        cost=8250000,
        runningcost=249,
        fixed_cost=46875,
        increase_maintenance_after_years=17,
        years_before_maintenance_max_reached=12,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['SR-Lord-Nelson-Tender'],
        liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='SR-Lord-Nelson-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1926,
        intro_month=8,
        retire_year=1940,
        retire_month=3,
        speed=145,
        length=5,
        weight=47,
        axles=4,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=17,
        years_before_maintenance_max_reached=12,
        constraint_prev=['SR-Lord-Nelson'],
        liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
