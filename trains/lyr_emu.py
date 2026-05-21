"""lyr-emu."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Third class only: https://en.wikipedia.org/wiki/LYR_electric_units#Liverpool_to_Ormskirk
_BLEND = 'trains/Railcars/lyr-emu-motor-lms.blend'
_UPSTREAM_DAT = 'trains/lyr-emu.dat'

SPECS = [
    Vehicle(
        name='L&YR-EMU-driving-motor',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        engine_type='electric',
        intro_year=1913,
        intro_month=2,
        retire_year=1935,
        retire_month=1,
        speed=89,
        length=10,
        weight=55,
        axles=4,
        power=552,
        gear=80,
        tractive_effort=30,
        payload=75,
        min_loading_time=20,
        max_loading_time=75,
        overcrowded_capacity=26,
        cost=13210000,
        runningcost=333,
        fixed_cost=17008,
        increase_maintenance_after_years=17,
        bidirectional=0,
        can_lead_from_rear=1,
        sound='x24tohayes-epb.wav',
        constraint_prev=['L&YR-EMU-driving-trailer', 'none'],
        constraint_next=['L&YR-EMU-driving-trailer'],
        payload_by_class=[0, 75],
        comfort_by_class=[0, 72],
        liverytype=['LYR-Black', 'LMS-Standard'],
        way_constraint_permissive=[1],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='L&YR-EMU-driving-trailer',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        engine_type='electric',
        intro_year=1913,
        intro_month=2,
        retire_year=1935,
        retire_month=1,
        speed=89,
        length=10,
        weight=29,
        axles=4,
        power=0,
        payload=85,
        min_loading_time=20,
        max_loading_time=75,
        overcrowded_capacity=29,
        cost=13210000,
        runningcost=1,
        fixed_cost=15726,
        increase_maintenance_after_years=17,
        bidirectional=0,
        can_lead_from_rear=1,
        sound='x24tohayes-epb.wav',
        constraint_prev=['L&YR-EMU-driving-motor'],
        constraint_next=['L&YR-EMU-driving-motor', 'none'],
        payload_by_class=[0, 85],
        comfort_by_class=[0, 72],
        liverytype=['LYR-Black', 'LMS-Standard'],
        way_constraint_permissive=[1],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
