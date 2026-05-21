"""wd-austerity-2-8-0."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/wd-austerity-2-8-0.blend'
_UPSTREAM_DAT = 'trains/wd-austerity-2-8-0.dat'

SPECS = [
    Vehicle(
        name='WD-Austerity-2-8-0',
        waytype='track',
        copyright='Kieron',
        freight='None',
        engine_type='steam',
        intro_year=1943,
        intro_month=10,
        retire_year=1954,
        retire_month=6,
        speed=90,
        length=7,
        weight=72,
        axle_load=17,
        power=384,
        tractive_effort=152,
        payload=0,
        cost=5060000,
        runningcost=262,
        fixed_cost=28217,
        increase_maintenance_after_years=9,
        years_before_maintenance_max_reached=10,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['WD-Austerity-2-8-0-Tender'],
        liverytype=['WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='WD-Austerity-2-8-0-Tender',
        waytype='track',
        copyright='Kieron',
        freight='None',
        intro_year=1943,
        intro_month=10,
        retire_year=1954,
        retire_month=6,
        speed=90,
        length=4,
        weight=53,
        axles=4,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=9,
        years_before_maintenance_max_reached=10,
        constraint_prev=['WD-Austerity-2-8-0'],
        liverytype=['WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
