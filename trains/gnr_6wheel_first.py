"""gnr-6wheel-first."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# "Non-lavatory
SPEC = Vehicle(
    name='GNR-6Wheel-First',
    waytype='track',
    copyright='Kieron/jamespetts',
    freight='Passagiere',
    intro_year=1876,
    intro_month=8,
    retire_year=1909,
    retire_month=11,
    speed=150,
    length=6,
    weight=14,
    axles=3,
    payload=24,
    min_loading_time=17,
    max_loading_time=47,
    overcrowded_capacity=0,
    cost=320000,
    runningcost=0,
    fixed_cost=377,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['4-wheel-1870s-fitted', '4-wheel-1870s-brake-fitted', '4-wheel-1870s-mail-fitted', '4-wheel-1870s-tpo-fitted', '4-wheel-sub-1870s-fitted', '4-wheel-sub-1870s-brake-front-fitted', 'GNR-6Wheel-First', 'GNR-6Wheel-cor-lav', 'GNR-6Wheel-Mail', 'GNR-6Wheel-tpo', 'GNR-6Wheel-brake-third-front', 'GNR-6Wheel-Guard', 'gnr-howlden-bogie-third', 'gnr-howlden-bogie-third-brake-front', 'gnr-howlden-bogie-non-lav', 'gnr-howlden-bogie-non-lav-brake-front', 'gnr-howlden-full-brake', 'gnr-non-cor-lav-elliptical', 'gnr-non-cor-lav-elliptical-brake-front', 'gnr-non-cor-full-brake', 'gnr-non-cor-mail', 'gnr-non-cor-lav-elliptical-composite', 'gnr-howlden-bogie-non-lav-second', 'gnr-howlden-bogie-non-lav-first', 'GNR-6Wheel-Third', 'GNR-6Wheel-Second', 'GNR-6Wheel-cor-lav-second', 'GNR-6Wheel-cor-lav-third', 'LNER-standard-51ft-t', 'LNER-standard-51ft-s', 'LNER-standard-51ft-bt4-for', 'LNER-standard-51ft-cl', 'LNER-standard-51ft-f', 'LNER-standard-51ft-f2', 'LNER-standard-51ft-com', 'gnr-suburban-4wheel-third', 'gnr-suburban-4wheel-second', 'gnr-suburban-4wheel-first', 'gnr-suburban-4wheel-brake-third-front'],
    constraint_next=['4-wheel-1870s-fitted', '4-wheel-1870s-brake-fitted', '4-wheel-1870s-mail-fitted', '4-wheel-1870s-tpo-fitted', '4-wheel-sub-1870s-fitted', '4-wheel-sub-1870s-brake-rear-fitted', 'GNR-6Wheel-First', 'GNR-6Wheel-cor-lav', 'GNR-6Wheel-Mail', 'GNR-6Wheel-tpo', 'GNR-6Wheel-brake-third-rear', 'GNR-6Wheel-Guard', 'gnr-howlden-bogie-third', 'gnr-howlden-bogie-third-brake-rear', 'gnr-howlden-bogie-non-lav', 'gnr-howlden-bogie-non-lav-brake-rear', 'gnr-howlden-full-brake', 'gnr-non-cor-lav-elliptical', 'gnr-non-cor-lav-elliptical-brake-rear', 'gnr-non-cor-full-brake', 'gnr-non-cor-mail', 'gnr-non-cor-lav-elliptical-composite', 'gnr-howlden-bogie-non-lav-second', 'gnr-howlden-bogie-non-lav-first', 'GNR-6Wheel-Third', 'GNR-6Wheel-Second', 'GNR-6Wheel-cor-lav-second', 'GNR-6Wheel-cor-lav-third', 'LNER-standard-51ft-t', 'LNER-standard-51ft-s', 'LNER-standard-51ft-bt4-rev', 'LNER-standard-51ft-cl', 'LNER-standard-51ft-f', 'LNER-standard-51ft-f2', 'LNER-standard-51ft-com', 'gnr-suburban-4wheel-third', 'gnr-suburban-4wheel-second', 'gnr-suburban-4wheel-first', 'gnr-suburban-4wheel-brake-third-rear'],
    payload_by_class=[0, 0, 0, 24],
    comfort_by_class=[0, 70, 72, 80],
    liverytype=['GNR-Standard', 'LNER-Standard'],
    blend='trains/Carriages/gnr-6wheel-cor-lav-second.blend',
    upstream_dat='trains/gnr-6wheel-first.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
