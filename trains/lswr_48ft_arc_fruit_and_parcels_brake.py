"""lswr-48ft-arc-fruit-and-parcels-brake."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Carriages/lswr-48ft.blend'
_UPSTREAM_DAT = 'trains/lswr-48ft-arc-fruit-and-parcels-brake.dat'

SPECS = [
    Vehicle(
        name='lswr-48ft-arc-fruit-brake',
        waytype='track',
        copyright='JamesPetts',
        freight='fruit',
        intro_year=1889,
        intro_month=6,
        retire_year=1899,
        retire_month=10,
        speed=160,
        length=8,
        weight=19.0,
        axles=4,
        payload=20,
        min_loading_time=300,
        max_loading_time=900,
        cost=675000,
        runningcost=0,
        fixed_cost=5604,
        bidirectional=1,
        can_lead_from_rear=0,
        liverytype=['LSWR-pea-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='lswr-48ft-arc-parcels-brake',
        waytype='track',
        copyright='JamesPetts',
        freight='Post',
        intro_year=1889,
        intro_month=6,
        retire_year=1899,
        retire_month=10,
        speed=160,
        length=8,
        weight=19.0,
        axles=4,
        payload=300,
        min_loading_time=35,
        max_loading_time=90,
        cost=675000,
        runningcost=0,
        fixed_cost=5081,
        bidirectional=1,
        can_lead_from_rear=0,
        liverytype=['LSWR-pea-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
