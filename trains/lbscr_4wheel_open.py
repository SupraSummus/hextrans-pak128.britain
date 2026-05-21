"""lbscr-4wheel-open."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.5and9models.co.uk/coaches.html
# See Hamilton Ellis p. 41 and Plate 6 III
# (between pages 31-32). This is probably a
# Craven coach from the later 1840s, built
# as fourth class after the 1844 Act.
#
# This five compartment vehicle would not
# be the same as the 17ft open carriage
# built as joint stock with the SER,
# described at p. 35 of Hamilton Ellis.
_BLEND = 'trains/Carriages/lbscr-4wheel-open-brake-front.blend'
_UPSTREAM_DAT = 'trains/lbscr-4wheel-open.dat'

SPECS = [
    Vehicle(
        name='LBSCR-4wheel-open',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1847,
        intro_month=2,
        retire_year=1856,
        retire_month=6,
        speed=125,
        length=4,
        weight=2,
        axles=2,
        brake_force=0,
        rolling_resistance=19,
        payload=50,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=25,
        cost=70000,
        runningcost=0,
        fixed_cost=146,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['any'],
        constraint_next=['any'],
        payload_by_class=[50],
        comfort_by_class=[20],
        upgrade=['LBSCR-4wheel-open-sided', 'LBSCR-4wheel-parliamentary-third', 'milk-van'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LBSCR-4wheel-open-brake',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1847,
        intro_month=2,
        retire_year=1856,
        retire_month=6,
        speed=110,
        length=4,
        weight=2,
        axles=2,
        brake_force=1,
        rolling_resistance=19,
        payload=48,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=20,
        cost=73000,
        runningcost=0,
        fixed_cost=4952,
        bidirectional=1,
        can_lead_from_rear=0,
        payload_by_class=[48],
        comfort_by_class=[20],
        upgrade=['LBSCR-4wheel-open-sided-brake', 'LBSCR-4wheel-parliamentary-third-brake', 'milk-van'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
