"""lner-gresley-express-mail."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Carriages/BACKUP-lner-gresley-articulated-triplet-restauraunt-fo.blend'
_UPSTREAM_DAT = 'trains/lner-gresley-express-mail.dat'

SPECS = [
    Vehicle(
        name='LNER-Gresley-Express-Mail',
        waytype='track',
        copyright='Kieron/James',
        freight='Post',
        intro_year=1923,
        intro_month=5,
        retire_year=1951,
        retire_month=2,
        speed=160,
        length=10,
        weight=31,
        axles=4,
        payload=600,
        min_loading_time=35,
        max_loading_time=180,
        cost=760000,
        runningcost=0,
        fixed_cost=317,
        increase_maintenance_after_years=15,
        years_before_maintenance_max_reached=30,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['LNER-Gresley-Express-Coach', 'LNER-Gresley-Express-Brake-front', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Mail', 'LNER-Gresley-Express-TPO', 'LNER-Gresley-Express-Parcel-Brake', 'LNER-Gresley-Express-Buffet', 'LNER-Gresley-Express-Coach-All-Doors', 'LNER-Gresley-Express-Brake-all-doors-front', 'gnr-clerestory-cor-63ft-5', 'gnr-clerestory-cor-brake-front-63ft-5', 'gnr-clerestory-dining-car', 'gnr-clerestory-cor-53ft-6', 'gnr-clerestory-cor-brake-front-53ft-6', 'gnr-clerestory-cor-full-brake-45ft', 'gnr-clerestory-cor-mail-45ft', 'gnr-clerestory-cor-tpo-45ft', 'gnr-gresley-cor', 'gnr-gresley-cor-brake-front', 'gnr-gresley-cor-dining', 'gnr-gresley-cor-parcels-brake', 'gnr-gresley-cor-mail', 'gnr-gresley-cor-tpo', 'pullman-1928-kitchen-first', 'pullman-1951-kitchen-first', 'LNER-Gresley-Express-first', 'LNER-Gresley-Express-Coach-All-Doors-first', 'gnr-gresley-cor-first', 'gnr-clerestory-cor-63ft-5-composite', 'gnr-clerestory-cor-63ft-5-first', 'gnr-clerestory-cor-composite-53ft-6'],
        constraint_next=['LNER-Gresley-Express-Coach', 'LNER-Gresley-Express-Brake-rear', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Mail', 'LNER-Gresley-Express-TPO', 'LNER-Gresley-Express-Parcel-Brake', 'LNER-Gresley-Express-Buffet', 'LNER-Gresley-Express-Coach-All-Doors', 'LNER-Gresley-Express-Brake-all-doors-rear', 'gnr-clerestory-cor-63ft-5', 'gnr-clerestory-cor-brake-rear-63ft-5', 'gnr-clerestory-dining-car', 'gnr-clerestory-cor-53ft-6', 'gnr-clerestory-cor-brake-rear-53ft-6', 'gnr-clerestory-cor-full-brake-45ft', 'gnr-clerestory-cor-mail-45ft', 'gnr-clerestory-cor-tpo-45ft', 'gnr-gresley-cor', 'gnr-gresley-cor-brake-rear', 'gnr-gresley-cor-dining', 'gnr-gresley-cor-parcels-brake', 'gnr-gresley-cor-mail', 'gnr-gresley-cor-tpo', 'pullman-1928-kitchen-first', 'pullman-1951-kitchen-first', 'LNER-Gresley-Express-first', 'LNER-Gresley-Express-Coach-All-Doors-first', 'gnr-gresley-cor-first', 'gnr-clerestory-cor-63ft-5-composite', 'gnr-clerestory-cor-63ft-5-first', 'gnr-clerestory-cor-composite-53ft-6'],
        liverytype=['LNER-Standard', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNER-Gresley-Express-TPO',
        waytype='track',
        copyright='Kieron/James',
        freight='Post',
        intro_year=1923,
        intro_month=5,
        retire_year=1959,
        retire_month=1,
        speed=160,
        length=10,
        weight=31,
        axles=4,
        payload=400,
        min_loading_time=35,
        max_loading_time=180,
        catering_level=1,
        cost=775000,
        runningcost=0,
        fixed_cost=24323,
        increase_maintenance_after_years=15,
        years_before_maintenance_max_reached=30,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['LNER-Gresley-Express-Coach', 'LNER-Gresley-Express-Brake-front', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Mail', 'LNER-Gresley-Express-TPO', 'LNER-Gresley-Express-Parcel-Brake', 'LNER-Gresley-Express-Buffet', 'LNER-Gresley-Express-Coach-All-Doors', 'LNER-Gresley-Express-Brake-all-doors-front', 'gnr-clerestory-cor-63ft-5', 'gnr-clerestory-cor-brake-front-63ft-5', 'gnr-clerestory-dining-car', 'gnr-clerestory-cor-53ft-6', 'gnr-clerestory-cor-brake-front-53ft-6', 'gnr-clerestory-cor-full-brake-45ft', 'gnr-clerestory-cor-mail-45ft', 'gnr-clerestory-cor-tpo-45ft', 'gnr-gresley-cor', 'gnr-gresley-cor-brake-front', 'gnr-gresley-cor-dining', 'gnr-gresley-cor-parcels-brake', 'gnr-gresley-cor-mail', 'gnr-gresley-cor-tpo', 'pullman-1928-kitchen-first', 'pullman-1951-kitchen-first', 'LNER-Gresley-Express-first', 'LNER-Gresley-Express-Coach-All-Doors-first', 'gnr-gresley-cor-first', 'gnr-clerestory-cor-63ft-5-composite', 'gnr-clerestory-cor-63ft-5-first', 'gnr-clerestory-cor-composite-53ft-6'],
        constraint_next=['LNER-Gresley-Express-Coach', 'LNER-Gresley-Express-Brake-rear', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Mail', 'LNER-Gresley-Express-TPO', 'LNER-Gresley-Express-Parcel-Brake', 'LNER-Gresley-Express-Buffet', 'LNER-Gresley-Express-Coach-All-Doors', 'LNER-Gresley-Express-Brake-all-doors-rear', 'gnr-clerestory-cor-63ft-5', 'gnr-clerestory-cor-brake-rear-63ft-5', 'gnr-clerestory-dining-car', 'gnr-clerestory-cor-53ft-6', 'gnr-clerestory-cor-brake-rear-53ft-6', 'gnr-clerestory-cor-full-brake-45ft', 'gnr-clerestory-cor-mail-45ft', 'gnr-clerestory-cor-tpo-45ft', 'gnr-gresley-cor', 'gnr-gresley-cor-brake-rear', 'gnr-gresley-cor-dining', 'gnr-gresley-cor-parcels-brake', 'gnr-gresley-cor-mail', 'gnr-gresley-cor-tpo', 'pullman-1928-kitchen-first', 'pullman-1951-kitchen-first', 'LNER-Gresley-Express-first', 'LNER-Gresley-Express-Coach-All-Doors-first', 'gnr-gresley-cor-first', 'gnr-clerestory-cor-63ft-5-composite', 'gnr-clerestory-cor-63ft-5-first', 'gnr-clerestory-cor-composite-53ft-6'],
        liverytype=['LNER-Standard', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
