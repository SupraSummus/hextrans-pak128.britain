"""lnwr-54ft-non-cor."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# D274: see Jenkinson (LNWR) p. 106
_BLEND = 'trains/Carriages/lnwr-54ft-non-cor-lms.blend'
_UPSTREAM_DAT = 'trains/lnwr-54ft-non-cor.dat'

SPECS = [
    Vehicle(
        name='LNWR-54ft-non-cor-lav-third',
        waytype='track',
        copyright='jamespetts',
        freight='Passagiere',
        intro_year=1907,
        intro_month=11,
        retire_year=1924,
        retire_month=4,
        speed=160,
        length=9,
        weight=28.4,
        axles=4,
        payload=72,
        min_loading_time=15,
        max_loading_time=45,
        overcrowded_capacity=22,
        cost=590000,
        runningcost=0,
        fixed_cost=710,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['LNWR-6Wheel-non-lav', 'LNWR-6Wheel-Mail', 'LNWR-6Wheel-tpo', 'LNWR-6Wheel-Guard', 'LNWR-6Wheel-lav', 'LNWR-6Wheel-brake-third', 'LNWR-8wheel-radial-lav', 'LNWR-8wheel-radial-brake', 'LNWR-8wheel-radial-mail', 'LNWR-8wheel-radial-tpo', 'LNWR-8wheel-radial-non-lav', 'LNWR-8wheel-radial-brake-lav-front', 'LNWR-8wheel-radial-full-brake', 'LNWR-42ft-non-cor-lav', 'LNWR-42ft-non-cor-non-lav', 'LNWR-42ft-non-cor-brake-front', 'LNWR-42ft-non-cor-brake-lav-front', 'LNWR-42ft-non-cor-mail', 'LNWR-42ft-non-cor-full-brake', 'LNWR-45ft-non-cor-lav', 'LNWR-45ft-non-cor-lav-brake', 'LNWR-50ft-non-cor-arc', 'LNWR-50ft-non-cor-arc-brake-front', 'LNWR-50ft-non-cor-eliptical-brake-front', 'LNWR-50ft-non-cor-eliptical', 'LNWR-57ft-non-cor-lav-brake-front', 'LNWR-57ft-non-cor-lav', 'LNWR-57ft-non-cor-brake-front', 'LNWR-57ft-non-cor', 'LNWR-6wheel-radial', 'LNWR-6wheel-radial-brake-third', 'LNWR-6wheel-radial-full-brake', 'LNWR-6wheel-radial-mail', 'LNWR-6wheel-radial-tpo', 'LMS-non-cor-lav', 'LMS-non-cor-non-lav', 'LMS-non-cor-brake-front', 'LMS-non-cor-brake-lav-front', 'LNWR-8wheel-radial-lav-first', 'LNWR-8wheel-radial-lav-tricomposite', 'LNWR-8wheel-radial-non-lav-composite', 'LNWR-8wheel-radial-non-lav-first', 'LNWR-6wheel-radial-first', 'LNWR-6wheel-radial-tricomposite', 'LNWR-42ft-non-cor-lav-first', 'LNWR-42ft-non-cor-lav-tricomposite', 'LNWR-42ft-non-cor-non-lav-first', 'LNWR-42ft-non-cor-non-lav-composite', 'LNWR-6Wheel-lav-tricomposite', 'LNWR-6Wheel-brake-composite', 'LNWR-45ft-non-cor-lav-tricomposite', 'LNWR-50ft-non-cor-arc-composite', 'LNWR-50ft-non-cor-arc-first', 'LNWR-50ft-non-cor-eliptical-composite-first-second', 'LNWR-50ft-non-cor-eliptical-composite-first-third', 'LNWR-54ft-non-cor-lav-third', 'LNWR-54ft-non-cor-lav-composite', 'LNWR-57ft-non-cor-first', 'LNWR-57ft-non-cor-composite', 'LMS-non-cor-lav-first', 'LMS-non-cor-non-lav-composite', 'LMS-non-cor-non-lav-first'],
        constraint_next=['LNWR-6Wheel-non-lav', 'LNWR-6Wheel-Mail', 'LNWR-6Wheel-tpo', 'LNWR-6Wheel-Guard', 'LNWR-6Wheel-lav', 'LNWR-6Wheel-brake-third', 'LNWR-8wheel-radial-lav', 'LNWR-8wheel-radial-brake', 'LNWR-8wheel-radial-mail', 'LNWR-8wheel-radial-tpo', 'LNWR-8wheel-radial-non-lav', 'LNWR-8wheel-radial-brake-lav-rear', 'LNWR-8wheel-radial-full-brake', 'LNWR-42ft-non-cor-lav', 'LNWR-42ft-non-cor-non-lav', 'LNWR-42ft-non-cor-brake-rear', 'LNWR-42ft-non-cor-brake-lav-rear', 'LNWR-42ft-non-cor-mail', 'LNWR-42ft-non-cor-full-brake', 'LNWR-45ft-non-cor-lav', 'LNWR-45ft-non-cor-lav-brake', 'LNWR-50ft-non-cor-arc', 'LNWR-50ft-non-cor-arc-brake-rear', 'LNWR-50ft-non-cor-eliptical-brake-rear', 'LNWR-50ft-non-cor-eliptical', 'LNWR-57ft-non-cor-lav-brake-rear', 'LNWR-57ft-non-cor-lav', 'LNWR-57ft-non-cor-brake-rear', 'LNWR-57ft-non-cor', 'LNWR-6wheel-radial', 'LNWR-6wheel-radial-brake-third', 'LNWR-6wheel-radial-full-brake', 'LNWR-6wheel-radial-mail', 'LNWR-6wheel-radial-tpo', 'LMS-non-cor-lav', 'LMS-non-cor-non-lav', 'LMS-non-cor-brake-rear', 'LMS-non-cor-brake-lav-rear', 'LNWR-8wheel-radial-lav-first', 'LNWR-8wheel-radial-lav-tricomposite', 'LNWR-8wheel-radial-non-lav-composite', 'LNWR-8wheel-radial-non-lav-first', 'LNWR-6wheel-radial-first', 'LNWR-6wheel-radial-tricomposite', 'LNWR-42ft-non-cor-lav-first', 'LNWR-42ft-non-cor-lav-tricomposite', 'LNWR-42ft-non-cor-non-lav-first', 'LNWR-42ft-non-cor-non-lav-composite', 'LNWR-6Wheel-lav-tricomposite', 'LNWR-6Wheel-brake-composite', 'LNWR-45ft-non-cor-lav-tricomposite', 'LNWR-50ft-non-cor-arc-composite', 'LNWR-50ft-non-cor-arc-first', 'LNWR-50ft-non-cor-eliptical-composite-first-second', 'LNWR-50ft-non-cor-eliptical-composite-first-third', 'LNWR-54ft-non-cor-lav-third', 'LNWR-54ft-non-cor-lav-composite', 'LNWR-57ft-non-cor-first', 'LNWR-57ft-non-cor-composite', 'LMS-non-cor-lav-first', 'LMS-non-cor-non-lav-composite', 'LMS-non-cor-non-lav-first'],
        payload_by_class=[0, 72, 0, 0],
        comfort_by_class=[0, 99, 103, 141],
        liverytype=['LNWR-Black', 'LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNWR-54ft-non-cor-lav-composite',
        waytype='track',
        copyright='jamespetts',
        freight='Passagiere',
        intro_year=1907,
        intro_month=11,
        retire_year=1912,
        retire_month=4,
        speed=160,
        length=9,
        weight=30.5,
        axles=4,
        payload=21,
        min_loading_time=15,
        max_loading_time=45,
        overcrowded_capacity=16,
        cost=595000,
        runningcost=0,
        fixed_cost=710,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['LNWR-6Wheel-non-lav', 'LNWR-6Wheel-Mail', 'LNWR-6Wheel-tpo', 'LNWR-6Wheel-Guard', 'LNWR-6Wheel-lav', 'LNWR-6Wheel-brake-third', 'LNWR-8wheel-radial-lav', 'LNWR-8wheel-radial-brake', 'LNWR-8wheel-radial-mail', 'LNWR-8wheel-radial-tpo', 'LNWR-8wheel-radial-non-lav', 'LNWR-8wheel-radial-brake-lav-front', 'LNWR-8wheel-radial-full-brake', 'LNWR-42ft-non-cor-lav', 'LNWR-42ft-non-cor-non-lav', 'LNWR-42ft-non-cor-brake-front', 'LNWR-42ft-non-cor-brake-lav-front', 'LNWR-42ft-non-cor-mail', 'LNWR-42ft-non-cor-full-brake', 'LNWR-45ft-non-cor-lav', 'LNWR-45ft-non-cor-lav-brake', 'LNWR-50ft-non-cor-arc', 'LNWR-50ft-non-cor-arc-brake-front', 'LNWR-50ft-non-cor-eliptical-brake-front', 'LNWR-50ft-non-cor-eliptical', 'LNWR-57ft-non-cor-lav-brake-front', 'LNWR-57ft-non-cor-lav', 'LNWR-57ft-non-cor-brake-front', 'LNWR-57ft-non-cor', 'LNWR-6wheel-radial', 'LNWR-6wheel-radial-brake-third', 'LNWR-6wheel-radial-full-brake', 'LNWR-6wheel-radial-mail', 'LNWR-6wheel-radial-tpo', 'LMS-non-cor-lav', 'LMS-non-cor-non-lav', 'LMS-non-cor-brake-front', 'LMS-non-cor-brake-lav-front', 'LNWR-8wheel-radial-lav-first', 'LNWR-8wheel-radial-lav-tricomposite', 'LNWR-8wheel-radial-non-lav-composite', 'LNWR-8wheel-radial-non-lav-first', 'LNWR-6wheel-radial-first', 'LNWR-6wheel-radial-tricomposite', 'LNWR-42ft-non-cor-lav-first', 'LNWR-42ft-non-cor-lav-tricomposite', 'LNWR-42ft-non-cor-non-lav-first', 'LNWR-42ft-non-cor-non-lav-composite', 'LNWR-6Wheel-lav-tricomposite', 'LNWR-6Wheel-brake-composite', 'LNWR-45ft-non-cor-lav-tricomposite', 'LNWR-50ft-non-cor-arc-composite', 'LNWR-50ft-non-cor-arc-first', 'LNWR-50ft-non-cor-eliptical-composite-first-second', 'LNWR-50ft-non-cor-eliptical-composite-first-third', 'LNWR-54ft-non-cor-lav-third', 'LNWR-54ft-non-cor-lav-composite', 'LNWR-57ft-non-cor-first', 'LNWR-57ft-non-cor-composite', 'LMS-non-cor-lav-first', 'LMS-non-cor-non-lav-composite', 'LMS-non-cor-non-lav-first'],
        constraint_next=['LNWR-6Wheel-non-lav', 'LNWR-6Wheel-Mail', 'LNWR-6Wheel-tpo', 'LNWR-6Wheel-Guard', 'LNWR-6Wheel-lav', 'LNWR-6Wheel-brake-third', 'LNWR-8wheel-radial-lav', 'LNWR-8wheel-radial-brake', 'LNWR-8wheel-radial-mail', 'LNWR-8wheel-radial-tpo', 'LNWR-8wheel-radial-non-lav', 'LNWR-8wheel-radial-brake-lav-rear', 'LNWR-8wheel-radial-full-brake', 'LNWR-42ft-non-cor-lav', 'LNWR-42ft-non-cor-non-lav', 'LNWR-42ft-non-cor-brake-rear', 'LNWR-42ft-non-cor-brake-lav-rear', 'LNWR-42ft-non-cor-mail', 'LNWR-42ft-non-cor-full-brake', 'LNWR-45ft-non-cor-lav', 'LNWR-45ft-non-cor-lav-brake', 'LNWR-50ft-non-cor-arc', 'LNWR-50ft-non-cor-arc-brake-rear', 'LNWR-50ft-non-cor-eliptical-brake-rear', 'LNWR-50ft-non-cor-eliptical', 'LNWR-57ft-non-cor-lav-brake-rear', 'LNWR-57ft-non-cor-lav', 'LNWR-57ft-non-cor-brake-rear', 'LNWR-57ft-non-cor', 'LNWR-6wheel-radial', 'LNWR-6wheel-radial-brake-third', 'LNWR-6wheel-radial-full-brake', 'LNWR-6wheel-radial-mail', 'LNWR-6wheel-radial-tpo', 'LMS-non-cor-lav', 'LMS-non-cor-non-lav', 'LMS-non-cor-brake-rear', 'LMS-non-cor-brake-lav-rear', 'LNWR-8wheel-radial-lav-first', 'LNWR-8wheel-radial-lav-tricomposite', 'LNWR-8wheel-radial-non-lav-composite', 'LNWR-8wheel-radial-non-lav-first', 'LNWR-6wheel-radial-first', 'LNWR-6wheel-radial-tricomposite', 'LNWR-42ft-non-cor-lav-first', 'LNWR-42ft-non-cor-lav-tricomposite', 'LNWR-42ft-non-cor-non-lav-first', 'LNWR-42ft-non-cor-non-lav-composite', 'LNWR-6Wheel-lav-tricomposite', 'LNWR-6Wheel-brake-composite', 'LNWR-45ft-non-cor-lav-tricomposite', 'LNWR-50ft-non-cor-arc-composite', 'LNWR-50ft-non-cor-arc-first', 'LNWR-50ft-non-cor-eliptical-composite-first-second', 'LNWR-50ft-non-cor-eliptical-composite-first-third', 'LNWR-54ft-non-cor-lav-third', 'LNWR-54ft-non-cor-lav-composite', 'LNWR-57ft-non-cor-first', 'LNWR-57ft-non-cor-composite', 'LMS-non-cor-lav-first', 'LMS-non-cor-non-lav-composite', 'LMS-non-cor-non-lav-first'],
        payload_by_class=[0, 10, 20, 21],
        comfort_by_class=[0, 78, 103, 141],
        liverytype=['LNWR-Black', 'LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
