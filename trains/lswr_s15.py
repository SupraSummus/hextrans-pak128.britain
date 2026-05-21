"""lswr-s15."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lswr-s15-austerity.blend'
_UPSTREAM_DAT = 'trains/lswr-s15.dat'

SPECS = [
    Vehicle(
        name='LSWR-S15',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1920,
        intro_month=2,
        retire_year=1936,
        retire_month=8,
        speed=90,
        length=6,
        weight=79,
        axle_load=19,
        power=438,
        tractive_effort=125,
        payload=0,
        cost=11486000,
        runningcost=241,
        fixed_cost=49572,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['LSWR-S15-Tender'],
        liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LSWR-S15-Tender',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        intro_year=1920,
        intro_month=2,
        retire_year=1936,
        retire_month=8,
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
        constraint_prev=['LSWR-S15'],
        liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
