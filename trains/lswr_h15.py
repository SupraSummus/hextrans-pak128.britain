"""lswr-h15."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lswr-h15-austerity.blend'
_UPSTREAM_DAT = 'trains/lswr-h15.dat'

SPECS = [
    Vehicle(
        name='LSWR-H15',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1914,
        intro_month=4,
        retire_year=1925,
        retire_month=11,
        speed=125,
        length=6,
        weight=81.2,
        axle_load=19,
        power=427,
        tractive_effort=117,
        payload=0,
        cost=11486000,
        runningcost=181,
        fixed_cost=49572,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['LSWR-H15-Tender'],
        liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LSWR-H15-Tender',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        intro_year=1914,
        intro_month=4,
        retire_year=1925,
        retire_month=11,
        speed=142,
        length=4,
        weight=57,
        axles=4,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=25,
        years_before_maintenance_max_reached=14,
        constraint_prev=['LSWR-H15'],
        liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
