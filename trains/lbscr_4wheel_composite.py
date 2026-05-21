"""lbscr-4wheel-composite."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See http://basilicafields.wordpress.com/2010/12/19/lbscr-carriages
# Four compartments (but compartment capacity as a third)
_BLEND = 'trains/Carriages/lbscr-4wheel-20ft-brake-composite.blend'
_UPSTREAM_DAT = 'trains/lbscr-4wheel-composite.dat'

SPECS = [
    Vehicle(
        name='LBSCR-4Wheel-composite',
        waytype='track',
        copyright='Kieron',
        freight='Passagiere',
        intro_year=1872,
        intro_month=4,
        retire_year=1877,
        retire_month=1,
        speed=145,
        length=5,
        weight=9.5,
        axles=2,
        brake_force=0,
        rolling_resistance=18,
        payload=16,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=0,
        cost=285000,
        runningcost=0,
        fixed_cost=339,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['any'],
        payload_by_class=[0, 0, 16, 12],
        comfort_by_class=[0, 62, 68, 77],
        liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'LBSCR-Late', 'SR-Olive-Green'],
        upgrade=['LBSCR-4Wheel-composite-fitted'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LBSCR-4Wheel-composite-fitted',
        waytype='track',
        copyright='Kieron',
        freight='Passagiere',
        intro_year=1875,
        intro_month=9,
        retire_year=1901,
        retire_month=1,
        speed=145,
        length=5,
        weight=9.7,
        axles=2,
        brake_force=5,
        rolling_resistance=18,
        payload=16,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=0,
        cost=340000,
        runningcost=0,
        fixed_cost=405,
        upgrade_price=5000,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['LBSCR-4Wheel-Brake-front-fitted', 'LBSCR-4Wheel-First-fitted', 'LBSCR-4Wheel-full-brake-fitted', 'LBSCR-4Wheel-Second-fitted', 'LBSCR-6Wheel-5-com', 'LBSCR-6Wheel-brake-front', 'LBSCR-6Wheel-guard', 'LBSCR-6Wheel-mail', 'LBSCR-balloon', 'LBSCR-balloon-brake-front', 'LBSCR-balloon-full-brake', 'LBSCR-non-cor-lav', 'LBSCR-non-cor-lav-brake-front', 'LBSCR-sub-bogie-48ft', 'LBSCR-sub-bogie-48ft-brake-front', 'LBSCR-sub-bogie-54ft', 'LBSCR-sub-bogie-54ft-brake-front', 'LBSCR-6Wheel-fruit-and-milk-van', 'LBSCR-6Wheel-fast-freight-van', 'LBSCR-6Wheel-5-com-second', 'LBSCR-6Wheel-composite', 'LBSCR-6Wheel-4-com-first', 'LBSCR-6Wheel-fruit-and-milk-van-brake', 'LBSCR-6Wheel-fast-freight-van-brake', 'LBSCR-4Wheel-third-fitted', 'LBSCR-4Wheel-composite-fitted', 'LBSCR-sub-bogie-48ft-composite', 'LBSCR-sub-bogie-48ft-first', 'LBSCR-non-cor-lav-first', 'LBSCR-sub-bogie-54ft-tricomposite', 'LBSCR-balloon-tricomposite', 'pullman-open-platform-kitchen', 'pullman-vestibule-kitchen', 'pullman-vestibule-12-wheel-kitchen', 'pullman-elliptical-8-wheel-kitchen', 'pullman-1908-kitchen', 'pullman-k-type-kitchen-first', 'pullman-1928-kitchen-first', 'pullman-1951-kitchen-first'],
        constraint_next=['LBSCR-4Wheel-Brake-rear-fitted', 'LBSCR-4Wheel-First-fitted', 'LBSCR-4Wheel-full-brake-fitted', 'LBSCR-4Wheel-Second-fitted', 'LBSCR-6Wheel-5-com', 'LBSCR-6Wheel-brake-rear', 'LBSCR-6Wheel-guard', 'LBSCR-6Wheel-mail', 'LBSCR-balloon', 'LBSCR-balloon-brake-rear', 'LBSCR-balloon-full-brake', 'LBSCR-non-cor-lav', 'LBSCR-non-cor-lav-brake-rear', 'LBSCR-sub-bogie-48ft', 'LBSCR-sub-bogie-48ft-brake-rear', 'LBSCR-sub-bogie-54ft', 'LBSCR-sub-bogie-54ft-brake-rear', 'LBSCR-6Wheel-fruit-and-milk-van', 'LBSCR-6Wheel-fast-freight-van', 'LBSCR-6Wheel-5-com-second', 'LBSCR-6Wheel-composite', 'LBSCR-6Wheel-4-com-first', 'LBSCR-6Wheel-fruit-and-milk-van-brake', 'LBSCR-6Wheel-fast-freight-van-brake', 'LBSCR-4Wheel-third-fitted', 'LBSCR-4Wheel-composite-fitted', 'LBSCR-sub-bogie-48ft-composite', 'LBSCR-sub-bogie-48ft-first', 'LBSCR-non-cor-lav-first', 'LBSCR-sub-bogie-54ft-tricomposite', 'LBSCR-balloon-tricomposite', 'pullman-open-platform-kitchen', 'pullman-vestibule-kitchen', 'pullman-vestibule-12-wheel-kitchen', 'pullman-elliptical-8-wheel-kitchen', 'pullman-1908-kitchen', 'pullman-k-type-kitchen-first', 'pullman-1928-kitchen-first', 'pullman-1951-kitchen-first'],
        payload_by_class=[0, 0, 16, 12],
        comfort_by_class=[0, 62, 68, 77],
        liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'LBSCR-Late', 'SR-Olive-Green'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
