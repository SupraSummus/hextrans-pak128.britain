"""pullman-vestibule."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Hamilton Ellis p. 103 and foot p. 101
# Based on "Prince", "Princess" and "Albert Victor" of the LBSCR
_BLEND = 'trains/Carriages/pullman-vestibule-12-wheel-mahogany.blend'
_UPSTREAM_DAT = 'trains/pullman-vestibule.dat'

SPECS = [
    Vehicle(
        name='pullman-vestibule-parlour',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1888,
        intro_month=12,
        retire_year=1908,
        retire_month=8,
        speed=160,
        length=10,
        weight=22.1,
        axles=4,
        payload=42,
        min_loading_time=40,
        max_loading_time=200,
        overcrowded_capacity=0,
        cost=655000,
        runningcost=0,
        fixed_cost=710,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['any'],
        payload_by_class=[0, 0, 0, 0, 42],
        comfort_by_class=[0, 0, 0, 0, 118],
        liverytype=['Pullman-Mahogany', 'Pullman-Bronze-Green', 'Pullman-Ivory-Umber'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='pullman-vestibule-kitchen',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1888,
        intro_month=12,
        retire_year=1908,
        retire_month=8,
        speed=160,
        length=10,
        weight=24.6,
        axles=4,
        payload=32,
        min_loading_time=40,
        max_loading_time=200,
        overcrowded_capacity=0,
        catering_level=5,
        cost=675000,
        runningcost=0,
        fixed_cost=1772,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['any'],
        payload_by_class=[0, 0, 0, 0, 32],
        comfort_by_class=[0, 0, 0, 0, 118],
        liverytype=['Pullman-Mahogany', 'Pullman-Bronze-Green', 'Pullman-Ivory-Umber'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
