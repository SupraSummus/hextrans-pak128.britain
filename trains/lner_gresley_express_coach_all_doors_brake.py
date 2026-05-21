"""lner-gresley-express-coach-all-doors-brake."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# This is the earlier version with compartment side
# doors, and with four a side in the thirds.
# Note: these were nominally three a side, but they
# had no armrests, so it was probable that they
# were treated as four a side.
# See Jenkinson pp. 314-5.
_BLEND = 'trains/Carriages/lner-gresley-express-coach.blend'
_UPSTREAM_DAT = 'trains/lner-gresley-express-coach-all-doors-brake.dat'

SPECS = [
    Vehicle(
        name='LNER-Gresley-Express-Brake-all-doors-front',
        waytype='track',
        copyright='Kieron',
        freight='Passagiere',
        intro_year=1923,
        intro_month=5,
        retire_year=1938,
        retire_month=7,
        speed=160,
        length=10,
        weight=32,
        axles=4,
        payload=36,
        min_loading_time=20,
        max_loading_time=50,
        overcrowded_capacity=16,
        cost=770000,
        runningcost=0,
        fixed_cost=5717,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['LNER-Gresley-Express-Coach', 'LNER-Gresley-Express-Brake-rear', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Mail', 'LNER-Gresley-Express-TPO', 'LNER-Gresley-Express-Parcel-Brake', 'LNER-Gresley-Express-Buffet', 'LNER-Gresley-Express-Coach-All-Doors', 'LNER-Gresley-Express-Brake-all-doors-rear', 'gnr-clerestory-cor-63ft-5', 'gnr-clerestory-cor-brake-rear-63ft-5', 'gnr-clerestory-dining-car', 'gnr-clerestory-cor-53ft-6', 'gnr-clerestory-cor-brake-rear-53ft-6', 'gnr-clerestory-cor-full-brake-45ft', 'gnr-clerestory-cor-mail-45ft', 'gnr-clerestory-cor-tpo-45ft', 'gnr-gresley-cor', 'gnr-gresley-cor-brake-rear', 'gnr-gresley-cor-dining', 'gnr-gresley-cor-parcels-brake', 'gnr-gresley-cor-mail', 'gnr-gresley-cor-tpo', 'pullman-1928-kitchen-first', 'pullman-1951-kitchen-first', 'pullman-k-type-kitchen-first', 'LNER-Gresley-Express-first', 'LNER-Gresley-Express-Coach-All-Doors-first', 'none'],
        payload_by_class=[0, 36, 0, 0],
        comfort_by_class=[0, 133, 133, 147],
        liverytype=['LNER-Standard', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNER-Gresley-Express-Brake-all-doors-rear',
        waytype='track',
        copyright='Kieron',
        freight='Passagiere',
        intro_year=1923,
        intro_month=5,
        retire_year=1938,
        retire_month=7,
        speed=160,
        length=10,
        weight=32,
        axles=4,
        payload=36,
        min_loading_time=20,
        max_loading_time=50,
        overcrowded_capacity=16,
        cost=770000,
        runningcost=0,
        fixed_cost=5717,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['LNER-Gresley-Express-Coach', 'LNER-Gresley-Express-Brake-front', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Mail', 'LNER-Gresley-Express-TPO', 'LNER-Gresley-Express-Parcel-Brake', 'LNER-Gresley-Express-Buffet', 'LNER-Gresley-Express-Coach-All-Doors', 'LNER-Gresley-Express-Brake-all-doors-front', 'gnr-clerestory-cor-63ft-5', 'gnr-clerestory-cor-brake-front-63ft-5', 'gnr-clerestory-dining-car', 'gnr-clerestory-cor-53ft-6', 'gnr-clerestory-cor-brake-front-53ft-6', 'gnr-clerestory-cor-full-brake-45ft', 'gnr-clerestory-cor-mail-45ft', 'gnr-clerestory-cor-tpo-45ft', 'gnr-gresley-cor', 'gnr-gresley-cor-brake-front', 'gnr-gresley-cor-dining', 'gnr-gresley-cor-parcels-brake', 'gnr-gresley-cor-mail', 'gnr-gresley-cor-tpo', 'pullman-1928-kitchen-first', 'pullman-1951-kitchen-first', 'pullman-k-type-kitchen-first', 'LNER-Gresley-Express-first', 'LNER-Gresley-Express-Coach-All-Doors-first'],
        payload_by_class=[0, 36, 0, 0],
        comfort_by_class=[0, 133, 133, 147],
        liverytype=['LNER-Standard', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
