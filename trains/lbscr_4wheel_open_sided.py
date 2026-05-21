"""lbscr-4wheel-open-sided."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.5and9models.co.uk/coaches.html
_BLEND = 'trains/Carriages/lbscr-4wheel-open.blend'
_UPSTREAM_DAT = 'trains/lbscr-4wheel-open-sided.dat'

SPECS = [
    Vehicle(
        name='LBSCR-4wheel-open-sided',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1850,
        intro_month=1,
        retire_year=1858,
        retire_month=11,
        speed=125,
        length=4,
        weight=3,
        axles=2,
        brake_force=0,
        rolling_resistance=19,
        payload=50,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=25,
        cost=90000,
        runningcost=0,
        fixed_cost=188,
        upgrade_price=15000,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['any'],
        constraint_next=['any'],
        payload_by_class=[0, 50],
        comfort_by_class=[0, 25],
        upgrade=['LBSCR-4wheel-parliamentary-third', 'milk-van'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LBSCR-4wheel-open-sided-brake',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1850,
        intro_month=1,
        retire_year=1858,
        retire_month=11,
        speed=125,
        length=4,
        weight=3,
        axles=2,
        brake_force=1,
        rolling_resistance=19,
        payload=48,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=24,
        cost=90000,
        runningcost=0,
        fixed_cost=4988,
        upgrade_price=15000,
        bidirectional=1,
        can_lead_from_rear=0,
        payload_by_class=[0, 48],
        comfort_by_class=[0, 25],
        upgrade=['LBSCR-4wheel-parliamentary-third-brake', 'milk-van'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
