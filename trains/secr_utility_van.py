"""secr-utility-van."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='secr-utility-van',
    waytype='track',
    copyright='James/JamesPetts',
    freight='Post',
    intro_year=1919,
    intro_month=1,
    retire_year=1928,
    retire_month=4,
    speed=160,
    length=5,
    weight=10.9,
    axles=2,
    payload=340,
    min_loading_time=45,
    max_loading_time=175,
    cost=580000,
    runningcost=0,
    fixed_cost=690,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['SR-Maunsell-Third', 'SR-Maunsell-Brake-front', 'SR-Maunsell-Dining', 'SR-Maunsell-Parcels', 'SR-Maunsell-Mail', 'SR-Maunsell-TPO', 'LSWR-Ironclad-Pantry', 'SR-Bulleid-Express-Coach', 'SR-Bulleid-Express-Brake-front', 'SR-Bulleid-Express-Dining', 'LSWR-Ironclad-Brake-front', 'LSWR-Ironclad', 'LSWR-Ironclad-Dining', 'LSWR-Ironclad-Mail', 'LSWR-Ironclad-TPO', 'LSWR-corridor', 'LSWR-corridor-brake-front', 'SR-Maunsell-Saloon', 'SR-Maunsell-Buffet', 'SR-Bulleid-Express-Coach-all-doors', 'SR-Bulleid-Express-brake-front-all-doors', 'SR-Bulleid-Express-Saloon', 'SR-Bulleid-Express-Buffet', 'LSWR-dining-saloon', 'SR-Maunsell-Parcels-Brake', 'secr-utility-van', 'LSWR-corridor-composite', 'LSWR-Ironclad-First', 'SR-Maunsell-First', 'SR-Maunsell-Composite'],
    constraint_next=['SR-Maunsell-Third', 'SR-Maunsell-Brake-rear', 'SR-Maunsell-Dining', 'SR-Maunsell-Parcels', 'SR-Maunsell-Mail', 'SR-Maunsell-TPO', 'LSWR-Ironclad-Pantry', 'SR-Bulleid-Express-Coach', 'SR-Bulleid-Express-Brake-rear', 'SR-Bulleid-Express-Dining', 'LSWR-Ironclad-Brake-rear', 'LSWR-Ironclad', 'LSWR-Ironclad-Dining', 'LSWR-Ironclad-Mail', 'LSWR-Ironclad-TPO', 'LSWR-corridor', 'LSWR-corridor-brake-rear', 'SR-Maunsell-Saloon', 'SR-Maunsell-Buffet', 'SR-Bulleid-Express-Coach-all-doors', 'SR-Bulleid-Express-brake-rear-all-doors', 'SR-Bulleid-Express-Saloon', 'SR-Bulleid-Express-Buffet', 'LSWR-dining-saloon', 'SR-Maunsell-Parcels-Brake', 'secr-utility-van', 'LSWR-corridor-composite', 'LSWR-Ironclad-First', 'SR-Maunsell-First', 'SR-Maunsell-Composite'],
    liverytype=['SECR-standard', 'SR-Olive-Green', 'SR-Malachite-Green', 'BR-Early'],
    blend='trains/Carriages/secr-utility-van-malachite.blend',
    upstream_dat='trains/secr-utility-van.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
