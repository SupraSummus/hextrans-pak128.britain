"""mr-45ft-clerestory-carriages."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Lacy & Dow vol. 2 pp. 370-1
# Before these were built, 6 wheel full brakes were used instead (d530).
_BLEND = 'trains/Carriages/mr-45ft-clerestory-full-brake.blend'
_UPSTREAM_DAT = 'trains/mr-45ft-clerestory-carriages.dat'

SPECS = [
    Vehicle(
        name='MR-45ft-clerestory-full-brake-d531',
        waytype='track',
        copyright='jamespetts',
        freight='Post',
        intro_year=1902,
        intro_month=10,
        retire_year=1917,
        retire_month=4,
        speed=160,
        length=8,
        weight=23,
        axles=4,
        payload=270,
        min_loading_time=35,
        max_loading_time=90,
        cost=470000,
        runningcost=0,
        fixed_cost=560,
        bidirectional=1,
        can_lead_from_rear=0,
        liverytype=['MR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='MR-45ft-clerestory-cor-full-brake-d536',
        waytype='track',
        copyright='jamespetts',
        freight='Post',
        intro_year=1906,
        intro_month=8,
        retire_year=1914,
        retire_month=11,
        speed=160,
        length=8,
        weight=23,
        axles=4,
        payload=270,
        min_loading_time=35,
        max_loading_time=90,
        cost=520000,
        runningcost=0,
        fixed_cost=619,
        bidirectional=1,
        can_lead_from_rear=0,
        liverytype=['MR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
