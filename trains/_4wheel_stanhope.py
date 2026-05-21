"""4wheel-stanhope."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Kidner p. 86. It is assumed that these were available
# earlier than the 1846 build date given for the prototype for this.
_BLEND = 'trains/Carriages/4wheel-stanhope.blend'
_UPSTREAM_DAT = 'trains/4wheel-stanhope.dat'

SPECS = [
    Vehicle(
        name='4wheel-stanhope',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1836,
        intro_month=2,
        retire_year=1847,
        retire_month=8,
        speed=125,
        length=2,
        weight=1.9,
        axles=2,
        brake_force=0,
        rolling_resistance=19,
        payload=36,
        min_loading_time=17,
        max_loading_time=60,
        overcrowded_capacity=0,
        cost=58000,
        runningcost=0,
        fixed_cost=48,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['any'],
        constraint_next=['any'],
        payload_by_class=[36],
        comfort_by_class=[10],
        liverytype=['LMR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='4wheel-stanhope-brake',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1836,
        intro_month=2,
        retire_year=1847,
        retire_month=8,
        speed=125,
        length=2,
        weight=1.9,
        axles=2,
        brake_force=1,
        rolling_resistance=19,
        payload=32,
        min_loading_time=17,
        max_loading_time=60,
        overcrowded_capacity=0,
        cost=58000,
        runningcost=0,
        fixed_cost=4848,
        bidirectional=1,
        can_lead_from_rear=0,
        payload_by_class=[32],
        comfort_by_class=[10],
        liverytype=['LMR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
