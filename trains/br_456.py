"""br-456."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Railcars/br-456-trailer-nse.blend'
_UPSTREAM_DAT = 'trains/br-456.dat'

SPECS = [
    Vehicle(
        name='BR-456-DMSO',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        engine_type='electric',
        intro_year=1990,
        intro_month=7,
        retire_year=1995,
        retire_month=6,
        speed=121,
        length=11,
        weight=41,
        axles=4,
        power=373,
        gear=80,
        tractive_effort=75,
        brake_force=30,
        rolling_resistance=13,
        payload=79,
        min_loading_time=15,
        max_loading_time=50,
        overcrowded_capacity=59,
        cost=1921000,
        runningcost=37,
        fixed_cost=11001,
        bidirectional=0,
        can_lead_from_rear=1,
        sound='video47-class-319.wav',
        constraint_prev=['BR-456-DTSO', 'BR-455-Driving-Rear', 'none'],
        constraint_next=['BR-456-DTSO'],
        payload_by_class=[0, 79],
        comfort_by_class=[0, 79],
        way_constraint_permissive=[0],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='BR-456-DTSO',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        engine_type='electric',
        intro_year=1990,
        intro_month=7,
        retire_year=1995,
        retire_month=6,
        speed=121,
        length=11,
        weight=31,
        axles=4,
        power=0,
        brake_force=23,
        rolling_resistance=13,
        payload=51,
        min_loading_time=15,
        max_loading_time=50,
        overcrowded_capacity=38,
        cost=1921000,
        runningcost=0,
        fixed_cost=4002,
        bidirectional=0,
        can_lead_from_rear=1,
        sound='video47-class-319.wav',
        constraint_prev=['BR-456-DMSO'],
        constraint_next=['BR-456-DMSO', 'BR-455-Driving-Front', 'none'],
        payload_by_class=[0, 51],
        comfort_by_class=[0, 79],
        way_constraint_permissive=[0],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
