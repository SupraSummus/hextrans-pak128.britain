"""pullman-open-platform."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Hamilton Ellis p. 91
# Also: https://www.flickr.com/photos/terry_browne/6821217682
_BLEND = 'trains/Carriages/pullman-open-platform-mr-dark.blend'
_UPSTREAM_DAT = 'trains/pullman-open-platform.dat'

SPECS = [
    Vehicle(
        name='pullman-open-platform-parlour-unfitted',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1874,
        intro_month=1,
        retire_year=1878,
        retire_month=2,
        speed=150,
        length=10,
        weight=21.8,
        axles=4,
        brake_force=0,
        payload=38,
        min_loading_time=45,
        max_loading_time=225,
        overcrowded_capacity=0,
        cost=605000,
        runningcost=0,
        fixed_cost=700,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['any'],
        payload_by_class=[0, 0, 0, 0, 38],
        comfort_by_class=[0, 0, 0, 0, 105],
        liverytype=['Pullman-Mahogany', 'Pullman-Bronze-Green', 'Pullman-Ivory-Umber', 'MR-Early', 'MR-Standard'],
        upgrade=['pullman-open-platform-parlour'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='pullman-open-platform-parlour',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1876,
        intro_month=3,
        retire_year=1889,
        retire_month=1,
        speed=150,
        length=10,
        weight=21.8,
        axles=4,
        payload=38,
        min_loading_time=45,
        max_loading_time=225,
        overcrowded_capacity=0,
        cost=605000,
        runningcost=0,
        fixed_cost=700,
        upgrade_price=120000,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['any'],
        payload_by_class=[0, 0, 0, 0, 38],
        comfort_by_class=[0, 0, 0, 0, 105],
        liverytype=['Pullman-Mahogany', 'Pullman-Bronze-Green', 'Pullman-Ivory-Umber', 'MR-Early', 'MR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='pullman-open-platform-kitchen',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1879,
        intro_month=7,
        retire_year=1889,
        retire_month=1,
        speed=150,
        length=10,
        weight=23.9,
        axles=4,
        payload=32,
        min_loading_time=45,
        max_loading_time=225,
        overcrowded_capacity=0,
        catering_level=5,
        cost=625000,
        runningcost=0,
        fixed_cost=1750,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['any'],
        payload_by_class=[0, 0, 0, 0, 32],
        comfort_by_class=[0, 0, 0, 0, 105],
        liverytype=['Pullman-Mahogany', 'Pullman-Bronze-Green', 'Pullman-Ivory-Umber', 'MR-Early', 'MR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
