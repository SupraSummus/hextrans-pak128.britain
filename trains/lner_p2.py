"""lner-p2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lner-p2-wartime.blend'
_UPSTREAM_DAT = 'trains/lner-p2.dat'

SPECS = [
    Vehicle(
        name='LNER-P2',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1934,
        intro_month=5,
        retire_year=1942,
        retire_month=1,
        speed=135,
        length=8,
        weight=107,
        axle_load=20,
        power=653,
        tractive_effort=200,
        way_wear_factor=147125,
        payload=0,
        cost=15206000,
        runningcost=376,
        fixed_cost=71679,
        increase_maintenance_after_years=13,
        years_before_maintenance_max_reached=10,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['LNER-P2-Tender'],
        liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNER-P2-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1934,
        intro_month=5,
        retire_year=1942,
        retire_month=1,
        speed=135,
        length=4,
        weight=57,
        axles=4,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=13,
        years_before_maintenance_max_reached=10,
        constraint_prev=['LNER-P2'],
        liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
