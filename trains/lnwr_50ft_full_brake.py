"""lnwr-50ft-full-brake."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# D312
_BLEND = 'trains/Carriages/lnwr-50ft-full-brake-lms.blend'
_UPSTREAM_DAT = 'trains/lnwr-50ft-full-brake.dat'

SPECS = [
    Vehicle(
        name='LNWR-50ft-cor-full-brake',
        waytype='track',
        copyright='Kieron/jamespetts',
        freight='Post',
        intro_year=1907,
        intro_month=4,
        retire_year=1923,
        retire_month=1,
        speed=160,
        length=9,
        weight=25,
        axles=4,
        payload=350,
        min_loading_time=35,
        max_loading_time=90,
        cost=630000,
        runningcost=0,
        fixed_cost=750,
        bidirectional=1,
        can_lead_from_rear=0,
        liverytype=['LNWR-Black', 'LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNWR-50ft-cor-mail',
        waytype='track',
        copyright='jamespetts',
        freight='Post',
        intro_year=1907,
        intro_month=4,
        retire_year=1923,
        retire_month=1,
        speed=160,
        length=9,
        weight=25,
        axles=4,
        payload=480,
        min_loading_time=35,
        max_loading_time=120,
        cost=630000,
        runningcost=0,
        fixed_cost=263,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['LNWR-45ft-cor-full-brake', 'LNWR-42ft-cor', 'LNWR-42ft-cor-brake-front', 'LNWR-42ft-cor-mail', 'LNWR-42ft-cor-tpo', 'LNWR-50ft-6in-diner-twin-saloon', 'LNWR-50ft-cor', 'LNWR-50ft-cor-brake', 'LNWR-60ft-6in-diner', 'LNWR-57ft-cor', 'LNWR-57ft-cor-brake-front', 'LNWR-57ft-cor-tpo', 'LNWR-57ft-cor-tea-car', 'LNWR-60ft-6in-diner-non-clerestory', 'LNWR-50ft-cor-mail', 'LNWR-50ft-cor-full-brake', 'LMS-period1-cor', 'LMS-period1-cor-brake-front', 'LMS-period1-cor-open', 'LMS-period1-cor-open-brake-front', 'LMS-period1-mail', 'LMS-period1-tpo', 'LMS-period1-full-brake', 'LMS-period1-cor-diner', 'LMS-open', 'LMS-full-brake', 'LMS-open-brake-front', 'LMS-diner', 'LMS-Mail', 'LMS-TPO', 'LMS-cor', 'LMS-cor-brake-front', 'LMS-buffet', 'LNWR-42ft-cor-first', 'LNWR-42ft-cor-composite', 'LNWR-42ft-cor-brake-composite-front', 'LNWR-50ft-cor-first', 'LNWR-57ft-cor-composite', 'LNWR-57ft-cor-first', 'LMS-period1-cor-open-first', 'LMS-period1-cor-first', 'LMS-period1-cor-composite'],
        constraint_next=['LNWR-45ft-cor-full-brake', 'LNWR-42ft-cor', 'LNWR-42ft-cor-brake-rear', 'LNWR-42ft-cor-mail', 'LNWR-42ft-cor-tpo', 'LNWR-50ft-6in-diner-twin-kitchen', 'LNWR-50ft-cor', 'LNWR-50ft-cor-brake', 'LNWR-60ft-6in-diner', 'LNWR-57ft-cor', 'LNWR-57ft-cor-brake-rear', 'LNWR-57ft-cor-tpo', 'LNWR-57ft-cor-tea-car', 'LNWR-60ft-6in-diner-non-clerestory', 'LNWR-50ft-cor-mail', 'LNWR-50ft-cor-full-brake', 'LMS-period1-cor', 'LMS-period1-cor-brake-rear', 'LMS-period1-cor-open', 'LMS-period1-cor-open-brake-rear', 'LMS-period1-mail', 'LMS-period1-tpo', 'LMS-period1-full-brake', 'LMS-period1-cor-diner', 'LMS-open', 'LMS-full-brake', 'LMS-open-brake-rear', 'LMS-diner', 'LMS-Mail', 'LMS-TPO', 'LMS-cor', 'LMS-cor-brake-rear', 'LMS-buffet', 'LNWR-42ft-cor-first', 'LNWR-42ft-cor-composite', 'LNWR-42ft-cor-brake-composite-rear', 'LNWR-50ft-cor-first', 'LNWR-57ft-cor-composite', 'LNWR-57ft-cor-first', 'LMS-period1-cor-open-first', 'LMS-period1-cor-first', 'LMS-period1-cor-composite'],
        liverytype=['LNWR-Black', 'LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
