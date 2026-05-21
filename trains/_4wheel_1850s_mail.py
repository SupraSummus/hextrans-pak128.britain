"""4wheel-1850s-mail."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Carriages/4wheel-1850.blend'
_UPSTREAM_DAT = 'trains/4wheel-1850s-mail.dat'

SPECS = [
    Vehicle(
        name='4-wheel-1850s-mail',
        waytype='track',
        copyright='James/jamespetts',
        freight='Post',
        intro_year=1850,
        intro_month=9,
        retire_year=1859,
        retire_month=10,
        speed=135,
        length=3,
        weight=8.0,
        axles=2,
        brake_force=0,
        rolling_resistance=19,
        payload=300,
        min_loading_time=35,
        max_loading_time=120,
        cost=144000,
        runningcost=0,
        fixed_cost=60,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['any'],
        constraint_next=['any'],
        liverytype=['LNWR-Early', 'MR-Early', 'MR-Standard', 'GNR-early', 'LSWR-Indian-red', 'GWR-early', 'GWR-two-tone'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='4-wheel-1850s-tpo',
        waytype='track',
        copyright='James',
        freight='Post',
        intro_year=1850,
        intro_month=9,
        retire_year=1859,
        retire_month=10,
        speed=135,
        length=3,
        weight=8.0,
        axles=2,
        brake_force=0,
        rolling_resistance=19,
        payload=240,
        min_loading_time=35,
        max_loading_time=120,
        catering_level=1,
        cost=153000,
        runningcost=0,
        fixed_cost=24064,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['any'],
        constraint_next=['any'],
        liverytype=['LNWR-Early', 'MR-Early', 'MR-Standard', 'GNR-early', 'LSWR-Indian-red', 'GWR-early', 'GWR-two-tone'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
