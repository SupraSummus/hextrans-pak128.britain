"""l&s-enclosed-carriage."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# These are Leicester & Swannington carriages;
# intended for minor railways. See Midland
# Railway Carriages by Lacy & Dow, pp. 8-9.
# https://cdn.globalauctionplatform.com/2a8bcfc7-99db-4e45-b8ea-a51c0101e0f0/316f84f8-a424-4388-b799-1e2436539fa7/original.jpg
_BLEND = 'trains/Carriages/l&s-enclosed-carriage.blend'
_UPSTREAM_DAT = 'trains/l&s-enclosed-carriage.dat'

SPECS = [
    Vehicle(
        name='l&s-enclosed-carriage',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1832,
        intro_month=7,
        retire_year=1845,
        retire_month=1,
        speed=55,
        length=3,
        weight=2.5,
        axles=2,
        brake_force=0,
        rolling_resistance=20,
        payload=18,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=9,
        cost=100000,
        runningcost=0,
        fixed_cost=83,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['l&s-enclosed-carriage', 'l&s-enclosed-carriage-brake-front', 'l&s-composite-carriage', 'l&s-composite-carriage-brake-front', 'l&s-open-carriage'],
        constraint_next=['l&s-enclosed-carriage', 'l&s-enclosed-carriage-brake-rear', 'l&s-composite-carriage', 'l&s-composite-carriage-brake-rear', 'l&s-open-carriage'],
        payload_by_class=[0, 0, 0, 18],
        comfort_by_class=[0, 0, 0, 40],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='l&s-enclosed-carriage-brake-front',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1832,
        intro_month=7,
        retire_year=1845,
        retire_month=1,
        speed=55,
        length=3,
        weight=2.5,
        axles=2,
        brake_force=1,
        rolling_resistance=20,
        payload=17,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=8,
        cost=110000,
        runningcost=0,
        fixed_cost=4892,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['l&s-enclosed-carriage', 'l&s-enclosed-carriage-brake-rear', 'l&s-composite-carriage', 'l&s-composite-carriage-brake-rear', 'l&s-open-carriage', 'none'],
        payload_by_class=[0, 0, 0, 17],
        comfort_by_class=[0, 0, 0, 40],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='l&s-enclosed-carriage-brake-rear',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1832,
        intro_month=7,
        retire_year=1845,
        retire_month=1,
        speed=55,
        length=3,
        weight=2.5,
        axles=2,
        brake_force=1,
        rolling_resistance=20,
        payload=17,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=8,
        cost=110000,
        runningcost=0,
        fixed_cost=4892,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['l&s-enclosed-carriage', 'l&s-enclosed-carriage-brake-front', 'l&s-composite-carriage', 'l&s-composite-carriage-brake-front', 'l&s-open-carriage'],
        payload_by_class=[0, 0, 0, 17],
        comfort_by_class=[0, 0, 0, 40],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
