"""br-114."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://railcar.co.uk/type/class-114/
_BLEND = 'trains/Railcars/br-114-dmbs-sypte.blend'
_UPSTREAM_DAT = 'trains/br-114.dat'

SPECS = [
    Vehicle(
        name='BR-114-DMBS',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        engine_type='diesel',
        intro_year=1956,
        intro_month=9,
        retire_year=1962,
        retire_month=1,
        speed=113,
        length=11,
        weight=38.1,
        axles=4,
        power=224,
        gear=50,
        tractive_effort=30,
        payload=62,
        min_loading_time=20,
        max_loading_time=60,
        overcrowded_capacity=65,
        cost=1273000,
        runningcost=224,
        fixed_cost=11292,
        bidirectional=0,
        can_lead_from_rear=1,
        smoke='Diesel',
        sound='spompeytransportvideo-class-117.wav',
        constraint_prev=['BR-121', 'BR-117-DMS', 'BR-104Rear', 'BR-128', 'BR-101-DMCL', 'BR-101-DTCL', 'BR-114-DTCL', 'BR-120-DMSL', 'BR-110-DMCL', 'none'],
        constraint_next=['BR-114-DTCL'],
        payload_by_class=[0, 62, 0, 0],
        comfort_by_class=[0, 80, 0, 107],
        liverytype=['BR-Revised', 'BR-Blue', 'BR-Large-Logo', 'SYPTE'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='BR-114-DTCL',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        engine_type='diesel',
        intro_year=1956,
        intro_month=9,
        retire_year=1962,
        retire_month=1,
        speed=113,
        length=11,
        weight=29.4,
        axles=4,
        power=0,
        gear=0,
        tractive_effort=30,
        payload=62,
        min_loading_time=20,
        max_loading_time=60,
        overcrowded_capacity=64,
        cost=621000,
        runningcost=0,
        fixed_cost=714,
        bidirectional=0,
        can_lead_from_rear=1,
        constraint_prev=['BR-114-DMBS'],
        constraint_next=['BR-121', 'BR-117-DMBS', 'BR-104Front', 'BR-128', 'BR-101-DMBS', 'BR-120-DMBC', 'BR-114-DMBS', 'BR-110-DMBC', 'none'],
        payload_by_class=[0, 62, 0, 12],
        comfort_by_class=[0, 80, 0, 107],
        liverytype=['BR-Revised', 'BR-Blue', 'BR-Large-Logo', 'SYPTE'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
