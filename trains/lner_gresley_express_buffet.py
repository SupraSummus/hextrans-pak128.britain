"""lner-gresley-express-buffet."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-Gresley-Express-Buffet',
    waytype='track',
    copyright='Kieron/jamespetts',
    freight='Passagiere',
    intro_year=1923,
    intro_month=5,
    retire_year=1951,
    retire_month=2,
    speed=160,
    length=10,
    weight=43,
    axles=4,
    payload=24,
    min_loading_time=25,
    max_loading_time=180,
    overcrowded_capacity=9,
    catering_level=3,
    cost=910000,
    runningcost=0,
    fixed_cost=19083,
    increase_maintenance_after_years=15,
    years_before_maintenance_max_reached=30,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['LNER-Gresley-Express-Coach', 'LNER-Gresley-Express-Brake-front', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Mail', 'LNER-Gresley-Express-TPO', 'LNER-Gresley-Express-Parcel-Brake', 'LNER-Gresley-Express-Buffet', 'LNER-Gresley-Express-Coach-All-Doors', 'LNER-Gresley-Express-Brake-all-doors-front', 'gnr-clerestory-cor-63ft-5', 'gnr-clerestory-cor-brake-front-63ft-5', 'gnr-clerestory-dining-car', 'gnr-clerestory-cor-53ft-6', 'gnr-clerestory-cor-brake-front-53ft-6', 'gnr-clerestory-cor-full-brake-45ft', 'gnr-clerestory-cor-mail-45ft', 'gnr-clerestory-cor-tpo-45ft', 'gnr-gresley-cor', 'gnr-gresley-cor-brake-front', 'gnr-gresley-cor-dining', 'gnr-gresley-cor-parcels-brake', 'gnr-gresley-cor-mail', 'gnr-gresley-cor-tpo', 'BR-Mk1-BG', 'BR-Mk1-BSK-front', 'BR-Mk1-BSO-front', 'BR-Mk1-RB', 'BR-Mk1-RMB', 'BR-Mk1-SK', 'BR-Mk1-TSO', 'BR-Mk2a-BSO', 'BR-Mk2a-RMB', 'BR-Mk2a-SO', 'BR-Mk2a-TSO', 'pullman-1928-kitchen-first', 'pullman-1951-kitchen-first', 'pullman-k-type-kitchen-first', 'LNER-Gresley-Express-first', 'LNER-Gresley-Express-Coach-All-Doors-first'],
    constraint_next=['LNER-Gresley-Express-Coach', 'LNER-Gresley-Express-Brake-rear', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Mail', 'LNER-Gresley-Express-TPO', 'LNER-Gresley-Express-Parcel-Brake', 'LNER-Gresley-Express-Buffet', 'LNER-Gresley-Express-Coach-All-Doors', 'LNER-Gresley-Express-Brake-all-doors-rear', 'gnr-clerestory-cor-63ft-5', 'gnr-clerestory-cor-brake-rear-63ft-5', 'gnr-clerestory-dining-car', 'gnr-clerestory-cor-53ft-6', 'gnr-clerestory-cor-brake-rear-53ft-6', 'gnr-clerestory-cor-full-brake-45ft', 'gnr-clerestory-cor-mail-45ft', 'gnr-clerestory-cor-tpo-45ft', 'gnr-gresley-cor', 'gnr-gresley-cor-brake-rear', 'gnr-gresley-cor-dining', 'gnr-gresley-cor-parcels-brake', 'gnr-gresley-cor-mail', 'gnr-gresley-cor-tpo', 'BR-Mk1-BG', 'BR-Mk1-BSK-rear', 'BR-Mk1-BSO-rear', 'BR-Mk1-RB', 'BR-Mk1-RMB', 'BR-Mk1-SK', 'BR-Mk1-TSO', 'BR-Mk2a-BSO', 'BR-Mk2a-RMB', 'BR-Mk2a-SO', 'BR-Mk2a-TSO', 'pullman-1928-kitchen-first', 'pullman-1951-kitchen-first', 'pullman-k-type-kitchen-first', 'LNER-Gresley-Express-first', 'LNER-Gresley-Express-Coach-All-Doors-first'],
    payload_by_class=[0, 24, 0, 0],
    comfort_by_class=[0, 133, 133, 133],
    liverytype=['LNER-Standard', 'BR-Early', 'BR-Revised', 'BR-Blue'],
    blend='trains/Carriages/lner-gresley-express-buffet-bg.blend',
    upstream_dat='trains/lner-gresley-express-buffet.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
