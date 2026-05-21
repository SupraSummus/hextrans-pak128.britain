"""lswr-30ft-full-brake-6-wheel-elliptical."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.roxeymouldings.co.uk/product/88/4c7-lswr-30ft-6-wheeled-full-brake-elliptical-roof-/
_BLEND = 'trains/Carriages/lswr-30ft-full-brake-6-wheel-elliptical-malachite.blend'
_UPSTREAM_DAT = 'trains/lswr-30ft-full-brake-6-wheel-elliptical.dat'

SPECS = [
    Vehicle(
        name='lswr-30ft-full-brake-6-wheel-elliptical',
        waytype='track',
        copyright='JamesPetts',
        freight='Post',
        intro_year=1893,
        intro_month=4,
        retire_year=1902,
        retire_month=9,
        speed=160,
        length=5,
        weight=13.5,
        axles=3,
        payload=185,
        min_loading_time=35,
        max_loading_time=90,
        cost=600000,
        runningcost=0,
        fixed_cost=714,
        bidirectional=1,
        can_lead_from_rear=0,
        liverytype=['LSWR-pea-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='lswr-30ft-fruit-brake-6-wheel-elliptical',
        waytype='track',
        copyright='JamesPetts',
        freight='fruit',
        intro_year=1893,
        intro_month=4,
        retire_year=1902,
        retire_month=94,
        speed=160,
        length=5,
        weight=13.5,
        axles=3,
        payload=34,
        min_loading_time=35,
        max_loading_time=90,
        cost=604200,
        runningcost=0,
        fixed_cost=715,
        bidirectional=1,
        can_lead_from_rear=0,
        liverytype=['LSWR-pea-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
