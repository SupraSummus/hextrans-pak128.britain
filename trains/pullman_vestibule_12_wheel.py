"""pullman-vestibule-12-wheel."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Hamilton Ellis p. 102 and Jenkinson p. 209
# Based on "The Arundel" and "Devonshire" used on the LBSCR
_BLEND = 'trains/Carriages/pullman-vestibule-12-wheel-mahogany.blend'
_UPSTREAM_DAT = 'trains/pullman-vestibule-12-wheel.dat'

SPECS = [
    Vehicle(
        name='pullman-vestibule-12-wheel-parlour',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1899,
        intro_month=3,
        retire_year=1908,
        retire_month=8,
        speed=160,
        length=11,
        weight=27.4,
        axles=4,
        payload=36,
        min_loading_time=40,
        max_loading_time=200,
        overcrowded_capacity=0,
        cost=781500,
        runningcost=0,
        fixed_cost=770,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['any'],
        payload_by_class=[0, 0, 0, 0, 36],
        comfort_by_class=[0, 0, 0, 0, 150],
        liverytype=['Pullman-Mahogany', 'Pullman-Bronze-Green', 'Pullman-Ivory-Umber', 'Pullman-Cream-Umber'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='pullman-vestibule-12-wheel-kitchen',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1899,
        intro_month=3,
        retire_year=1908,
        retire_month=8,
        speed=160,
        length=11,
        weight=31.5,
        axles=4,
        payload=32,
        min_loading_time=40,
        max_loading_time=200,
        overcrowded_capacity=0,
        catering_level=5,
        cost=795000,
        runningcost=0,
        fixed_cost=1822,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['any'],
        payload_by_class=[0, 0, 0, 0, 32],
        comfort_by_class=[0, 0, 0, 0, 150],
        liverytype=['Pullman-Mahogany', 'Pullman-Bronze-Green', 'Pullman-Ivory-Umber', 'Pullman-Cream-Umber'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
