"""6wheel-stanhope."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Hamilton Ellis p. 39. Full details are not given.
_BLEND = 'trains/Carriages/6wheel-stanhope.blend'
_UPSTREAM_DAT = 'trains/6wheel-stanhope.dat'

SPECS = [
    Vehicle(
        name='6wheel-stanhope',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1841,
        intro_month=11,
        retire_year=1852,
        retire_month=9,
        speed=125,
        length=4,
        weight=3.1,
        axles=2,
        brake_force=0,
        rolling_resistance=19,
        payload=55,
        min_loading_time=17,
        max_loading_time=70,
        overcrowded_capacity=0,
        cost=58000,
        runningcost=0,
        fixed_cost=48,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['any'],
        constraint_next=['any'],
        payload_by_class=[55],
        comfort_by_class=[10],
        liverytype=['LMR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='6wheel-stanhope-brake',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1841,
        intro_month=11,
        retire_year=1852,
        retire_month=9,
        speed=125,
        length=4,
        weight=3.2,
        axles=2,
        brake_force=2,
        rolling_resistance=19,
        payload=52,
        min_loading_time=17,
        max_loading_time=70,
        overcrowded_capacity=0,
        cost=58000,
        runningcost=0,
        fixed_cost=4848,
        bidirectional=1,
        can_lead_from_rear=0,
        payload_by_class=[52],
        comfort_by_class=[10],
        liverytype=['LMR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
