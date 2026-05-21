"""gnr-6wheel-cor-lav."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Hamilton-Ellis pp. 119-120
# Initially first class only.
# Second/third class introduced 1888
_BLEND = 'trains/Carriages/gnr-6wheel-cor-lav-second.blend'
_UPSTREAM_DAT = 'trains/gnr-6wheel-cor-lav.dat'

SPECS = [
    Vehicle(
        name='GNR-6Wheel-cor-lav',
        waytype='track',
        copyright='Kieron/jamespetts',
        freight='Passagiere',
        intro_year=1881,
        intro_month=1,
        retire_year=1909,
        retire_month=11,
        speed=150,
        length=6,
        weight=17,
        axles=3,
        payload=16,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=0,
        cost=400000,
        runningcost=0,
        fixed_cost=475,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['4-wheel-1870s-fitted', '4-wheel-1870s-brake-fitted', '4-wheel-1870s-mail-fitted', '4-wheel-1870s-tpo-fitted', '4-wheel-sub-1870s-fitted', '4-wheel-sub-1870s-brake-front-fitted', 'GNR-6Wheel-First', 'GNR-6Wheel-cor-lav', 'GNR-6Wheel-Mail', 'GNR-6Wheel-tpo', 'GNR-6Wheel-brake-third-front', 'GNR-6Wheel-Guard', 'gnr-howlden-bogie-third', 'gnr-howlden-bogie-third-brake-front', 'gnr-howlden-bogie-non-lav', 'gnr-howlden-bogie-non-lav-brake-front', 'gnr-howlden-full-brake', 'gnr-non-cor-lav-elliptical', 'gnr-non-cor-lav-elliptical-brake-front', 'gnr-non-cor-full-brake', 'gnr-non-cor-mail', 'gnr-non-cor-lav-elliptical-composite', 'gnr-howlden-bogie-non-lav-second', 'gnr-howlden-bogie-non-lav-first', 'GNR-6Wheel-Third', 'GNR-6Wheel-Second', 'GNR-6Wheel-cor-lav-second', 'GNR-6Wheel-cor-lav-third'],
        constraint_next=['4-wheel-1870s-fitted', '4-wheel-1870s-brake-fitted', '4-wheel-1870s-mail-fitted', '4-wheel-1870s-tpo-fitted', '4-wheel-sub-1870s-fitted', '4-wheel-sub-1870s-brake-rear-fitted', 'GNR-6Wheel-First', 'GNR-6Wheel-cor-lav', 'GNR-6Wheel-Mail', 'GNR-6Wheel-tpo', 'GNR-6Wheel-brake-third-rear', 'GNR-6Wheel-Guard', 'gnr-howlden-bogie-third', 'gnr-howlden-bogie-third-brake-rear', 'gnr-howlden-bogie-non-lav', 'gnr-howlden-bogie-non-lav-brake-rear', 'gnr-howlden-full-brake', 'gnr-non-cor-lav-elliptical', 'gnr-non-cor-lav-elliptical-brake-rear', 'gnr-non-cor-full-brake', 'gnr-non-cor-mail', 'gnr-non-cor-lav-elliptical-composite', 'gnr-howlden-bogie-non-lav-second', 'gnr-howlden-bogie-non-lav-first', 'GNR-6Wheel-Third', 'GNR-6Wheel-Second', 'GNR-6Wheel-cor-lav-second', 'GNR-6Wheel-cor-lav-third'],
        payload_by_class=[0, 0, 0, 16],
        comfort_by_class=[0, 81, 83, 92],
        liverytype=['GNR-Standard', 'LNER-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='GNR-6Wheel-cor-lav-second',
        waytype='track',
        copyright='Kieron/jamespetts',
        freight='Passagiere',
        intro_year=1888,
        intro_month=7,
        retire_year=1909,
        retire_month=11,
        speed=150,
        length=6,
        weight=17,
        axles=3,
        payload=30,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=15,
        cost=398500,
        runningcost=0,
        fixed_cost=474,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['4-wheel-1870s-fitted', '4-wheel-1870s-brake-fitted', '4-wheel-1870s-mail-fitted', '4-wheel-1870s-tpo-fitted', '4-wheel-sub-1870s-fitted', '4-wheel-sub-1870s-brake-front-fitted', 'GNR-6Wheel-First', 'GNR-6Wheel-cor-lav', 'GNR-6Wheel-Mail', 'GNR-6Wheel-tpo', 'GNR-6Wheel-brake-third-front', 'GNR-6Wheel-Guard', 'gnr-howlden-bogie-third', 'gnr-howlden-bogie-third-brake-front', 'gnr-howlden-bogie-non-lav', 'gnr-howlden-bogie-non-lav-brake-front', 'gnr-howlden-full-brake', 'gnr-non-cor-lav-elliptical', 'gnr-non-cor-lav-elliptical-brake-front', 'gnr-non-cor-full-brake', 'gnr-non-cor-mail', 'gnr-non-cor-lav-elliptical-composite', 'gnr-howlden-bogie-non-lav-second', 'gnr-howlden-bogie-non-lav-first', 'GNR-6Wheel-Third', 'GNR-6Wheel-Second', 'GNR-6Wheel-cor-lav-second', 'GNR-6Wheel-cor-lav-third'],
        constraint_next=['4-wheel-1870s-fitted', '4-wheel-1870s-brake-fitted', '4-wheel-1870s-mail-fitted', '4-wheel-1870s-tpo-fitted', '4-wheel-sub-1870s-fitted', '4-wheel-sub-1870s-brake-rear-fitted', 'GNR-6Wheel-First', 'GNR-6Wheel-cor-lav', 'GNR-6Wheel-Mail', 'GNR-6Wheel-tpo', 'GNR-6Wheel-brake-third-rear', 'GNR-6Wheel-Guard', 'gnr-howlden-bogie-third', 'gnr-howlden-bogie-third-brake-rear', 'gnr-howlden-bogie-non-lav', 'gnr-howlden-bogie-non-lav-brake-rear', 'gnr-howlden-full-brake', 'gnr-non-cor-lav-elliptical', 'gnr-non-cor-lav-elliptical-brake-rear', 'gnr-non-cor-full-brake', 'gnr-non-cor-mail', 'gnr-non-cor-lav-elliptical-composite', 'gnr-howlden-bogie-non-lav-second', 'gnr-howlden-bogie-non-lav-first', 'GNR-6Wheel-Third', 'GNR-6Wheel-Second', 'GNR-6Wheel-cor-lav-second', 'GNR-6Wheel-cor-lav-third'],
        payload_by_class=[0, 0, 30, 0],
        comfort_by_class=[0, 81, 83, 92],
        liverytype=['GNR-Standard', 'LNER-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='GNR-6Wheel-cor-lav-third',
        waytype='track',
        copyright='Kieron/jamespetts',
        freight='Passagiere',
        intro_year=1888,
        intro_month=7,
        retire_year=1909,
        retire_month=11,
        speed=150,
        length=6,
        weight=17,
        axles=3,
        payload=30,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=15,
        cost=397000,
        runningcost=0,
        fixed_cost=473,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['4-wheel-1870s-fitted', '4-wheel-1870s-brake-fitted', '4-wheel-1870s-mail-fitted', '4-wheel-1870s-tpo-fitted', '4-wheel-sub-1870s-fitted', '4-wheel-sub-1870s-brake-front-fitted', 'GNR-6Wheel-First', 'GNR-6Wheel-cor-lav', 'GNR-6Wheel-Mail', 'GNR-6Wheel-tpo', 'GNR-6Wheel-brake-third-front', 'GNR-6Wheel-Guard', 'gnr-howlden-bogie-third', 'gnr-howlden-bogie-third-brake-front', 'gnr-howlden-bogie-non-lav', 'gnr-howlden-bogie-non-lav-brake-front', 'gnr-howlden-full-brake', 'gnr-non-cor-lav-elliptical', 'gnr-non-cor-lav-elliptical-brake-front', 'gnr-non-cor-full-brake', 'gnr-non-cor-mail', 'gnr-non-cor-lav-elliptical-composite', 'gnr-howlden-bogie-non-lav-second', 'gnr-howlden-bogie-non-lav-first', 'GNR-6Wheel-Third', 'GNR-6Wheel-Second', 'GNR-6Wheel-cor-lav-second', 'GNR-6Wheel-cor-lav-third'],
        constraint_next=['4-wheel-1870s-fitted', '4-wheel-1870s-brake-fitted', '4-wheel-1870s-mail-fitted', '4-wheel-1870s-tpo-fitted', '4-wheel-sub-1870s-fitted', '4-wheel-sub-1870s-brake-rear-fitted', 'GNR-6Wheel-First', 'GNR-6Wheel-cor-lav', 'GNR-6Wheel-Mail', 'GNR-6Wheel-tpo', 'GNR-6Wheel-brake-third-rear', 'GNR-6Wheel-Guard', 'gnr-howlden-bogie-third', 'gnr-howlden-bogie-third-brake-rear', 'gnr-howlden-bogie-non-lav', 'gnr-howlden-bogie-non-lav-brake-rear', 'gnr-howlden-full-brake', 'gnr-non-cor-lav-elliptical', 'gnr-non-cor-lav-elliptical-brake-rear', 'gnr-non-cor-full-brake', 'gnr-non-cor-mail', 'gnr-non-cor-lav-elliptical-composite', 'gnr-howlden-bogie-non-lav-second', 'gnr-howlden-bogie-non-lav-first', 'GNR-6Wheel-Third', 'GNR-6Wheel-Second', 'GNR-6Wheel-cor-lav-second', 'GNR-6Wheel-cor-lav-third'],
        payload_by_class=[0, 0, 0, 30],
        comfort_by_class=[0, 81, 83, 92],
        liverytype=['GNR-Standard', 'LNER-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
