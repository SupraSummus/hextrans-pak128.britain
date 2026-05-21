"""lner-d49."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lner-d49-wartime.blend'
_UPSTREAM_DAT = 'trains/lner-d49.dat'

SPECS = [
    Vehicle(
        name='LNER-D49',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1927,
        intro_month=10,
        retire_year=1935,
        retire_month=12,
        speed=145,
        length=6,
        weight=65,
        axle_load=22,
        power=386,
        tractive_effort=96,
        way_wear_factor=89375,
        payload=0,
        cost=6943104,
        runningcost=219,
        fixed_cost=29786,
        increase_maintenance_after_years=19,
        years_before_maintenance_max_reached=13,
        smoke='Steam',
        constraint_next=['LNER-D49-Tender'],
        liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNER-D49-Tender',
        waytype='track',
        copyright='Kieron/jamespetts',
        freight='None',
        intro_year=1927,
        intro_month=10,
        retire_year=1935,
        retire_month=12,
        speed=145,
        length=4,
        weight=52,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=18,
        years_before_maintenance_max_reached=14,
        constraint_prev=['LNER-D49'],
        liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
