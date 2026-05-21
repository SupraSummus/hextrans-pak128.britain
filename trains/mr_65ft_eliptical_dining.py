"""mr-65ft-eliptical-dining."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Lacy & Dow vol. 2 pp. 456-7
# Anglo-Scottish joint stock.
SPEC = Vehicle(
    name='MR-65ft-eliptical-dining-d1196',
    waytype='track',
    copyright='jamespetts',
    freight='Passagiere',
    intro_year=1917,
    intro_month=4,
    retire_year=1923,
    retire_month=1,
    speed=160,
    length=11,
    weight=32.5,
    axles=6,
    rolling_resistance=17,
    payload=24,
    min_loading_time=25,
    max_loading_time=120,
    catering_level=4,
    cost=887000,
    runningcost=0,
    fixed_cost=19056,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['LNWR-45ft-cor-full-brake', 'LNWR-42ft-cor', 'LNWR-42ft-cor-brake-front', 'LNWR-42ft-cor-mail', 'LNWR-42ft-cor-tpo', 'LNWR-50ft-6in-diner-twin-saloon', 'LNWR-50ft-cor', 'LNWR-50ft-cor-brake', 'LNWR-60ft-6in-diner', 'LNWR-57ft-cor', 'LNWR-57ft-cor-brake-front', 'LNWR-57ft-cor-tpo', 'LNWR-57ft-cor-tea-car', 'LNWR-60ft-6in-diner-non-clerestory', 'LNWR-50ft-cor-mail', 'LNWR-50ft-cor-full-brake', 'LMS-period1-cor', 'LMS-period1-cor-brake-front', 'LMS-period1-cor-open', 'LMS-period1-cor-open-brake-front', 'LMS-period1-mail', 'LMS-period1-tpo', 'LMS-period1-full-brake', 'LMS-period1-cor-diner', 'LMS-open', 'LMS-full-brake', 'LMS-open-brake-front', 'LMS-diner', 'LMS-Mail', 'LMS-TPO', 'LMS-cor', 'LMS-cor-brake-front', 'LMS-buffet', 'MR-31ft-clerestory-cor-brake-d568', 'MR-48ft-clerestory-cor-d575', 'MR-48ft-clerestory-cor-lav-brake-front', 'MR-48ft-clerestory-full-brake-d1067', 'MR-54ft-clerestory-cor-d560', 'MR-54ft-clerestory-cor-brake-d467-front', 'MR-54ft-clerestory-mini-restaurant-brake-d443-front', 'MR-54ft-clerestory-open-vestibule-d595', 'MR-54ft-clerestory-open-vestibule-brake-d594-front', 'MR-54ft-eliptical-cor-d1047', 'MR-54ft-eliptical-cor-brake-front-d1048', 'MR-54ft-eliptical-full-brake-d1114', 'MR-60ft-clerestory-kitchen-dining-d444', 'MR-65ft-clerestory-dining-d575', 'MR-65ft-eliptical-dining-d1196', 'LNWR-42ft-cor-first', 'LNWR-42ft-cor-composite', 'LNWR-42ft-cor-brake-composite-front', 'LNWR-50ft-cor-first', 'LNWR-57ft-cor-composite', 'LNWR-57ft-cor-first', 'LMS-period1-cor-open-first', 'LMS-period1-cor-first', 'LMS-period1-cor-composite', 'LMS-open-first', 'LMS-open-composite', 'LMS-cor-first', 'LMS-cor-composite', 'MR-54ft-clerestory-cor-composite-d593', 'MR-54ft-clerestory-cor-first-d600', 'MR-54ft-eliptical-cor-brake-composite-front-d1046'],
    constraint_next=['LNWR-45ft-cor-full-brake', 'LNWR-42ft-cor', 'LNWR-42ft-cor-brake-rear', 'LNWR-42ft-cor-mail', 'LNWR-42ft-cor-tpo', 'LNWR-50ft-6in-diner-twin-kitchen', 'LNWR-50ft-cor', 'LNWR-50ft-cor-brake', 'LNWR-60ft-6in-diner', 'LNWR-57ft-cor', 'LNWR-57ft-cor-brake-rear', 'LNWR-57ft-cor-tpo', 'LNWR-57ft-cor-tea-car', 'LNWR-60ft-6in-diner-non-clerestory', 'LNWR-50ft-cor-mail', 'LNWR-50ft-cor-full-brake', 'LMS-period1-cor', 'LMS-period1-cor-brake-rear', 'LMS-period1-cor-open', 'LMS-period1-cor-open-brake-rear', 'LMS-period1-mail', 'LMS-period1-tpo', 'LMS-period1-full-brake', 'LMS-period1-cor-diner', 'LMS-open', 'LMS-full-brake', 'LMS-open-brake-rear', 'LMS-diner', 'LMS-Mail', 'LMS-TPO', 'LMS-cor', 'LMS-cor-brake-rear', 'LMS-buffet', 'MR-31ft-clerestory-cor-brake-d568', 'MR-48ft-clerestory-cor-d575', 'MR-48ft-clerestory-cor-lav-brake-rear', 'MR-48ft-clerestory-full-brake-d1067', 'MR-54ft-clerestory-cor-d560', 'MR-54ft-clerestory-cor-brake-d467-rear', 'MR-54ft-clerestory-mini-restaurant-brake-d443-rear', 'MR-54ft-clerestory-open-vestibule-d595', 'MR-54ft-clerestory-open-vestibule-brake-d594-rear', 'MR-54ft-eliptical-cor-d1047', 'MR-54ft-eliptical-cor-brake-rear-d1048', 'MR-54ft-eliptical-full-brake-d1114', 'MR-60ft-clerestory-kitchen-dining-d444', 'MR-65ft-clerestory-dining-d575', 'MR-65ft-eliptical-dining-d1196', 'LNWR-42ft-cor-first', 'LNWR-42ft-cor-composite', 'LNWR-42ft-cor-brake-composite-rear', 'LNWR-50ft-cor-first', 'LNWR-57ft-cor-composite', 'LNWR-57ft-cor-first', 'LMS-period1-cor-open-first', 'LMS-period1-cor-first', 'LMS-period1-cor-composite', 'LMS-open-first', 'LMS-open-composite', 'LMS-cor-first', 'LMS-cor-composite', 'MR-54ft-clerestory-cor-composite-d593', 'MR-54ft-clerestory-cor-first-d600', 'MR-54ft-eliptical-cor-brake-composite-rear-d1046'],
    payload_by_class=[0, 24, 0, 0],
    comfort_by_class=[0, 135, 0, 150],
    liverytype=['MR-Standard', 'BR-Early'],
    blend='trains/Carriages/mr-65ft-eliptical-dining-br.blend',
    upstream_dat='trains/mr-65ft-eliptical-dining.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
