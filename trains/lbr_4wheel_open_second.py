"""lbr-4wheel-open-second."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See http://gerald-massey.org.uk/Railway/c13_operational.htm
# Exact details not given.
_BLEND = 'trains/Carriages/lbr-4wheel-open-second.blend'
_UPSTREAM_DAT = 'trains/lbr-4wheel-open-second.dat'

SPECS = [
    Vehicle(
        name='lbr-4wheel-open-second',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1837,
        intro_month=7,
        retire_year=1844,
        retire_month=5,
        speed=125,
        length=2,
        weight=2.1,
        axles=2,
        brake_force=0,
        rolling_resistance=19,
        payload=24,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=9,
        cost=136000,
        runningcost=0,
        fixed_cost=283,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['any'],
        constraint_next=['any'],
        payload_by_class=[0, 0, 24],
        comfort_by_class=[0, 0, 24],
        liverytype=['LMR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='lbr-4wheel-open-second-brake',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        intro_year=1837,
        intro_month=7,
        retire_year=1844,
        retire_month=5,
        speed=125,
        length=2,
        weight=2.1,
        axles=2,
        brake_force=1,
        rolling_resistance=19,
        payload=24,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=9,
        cost=137000,
        runningcost=0,
        fixed_cost=5085,
        bidirectional=1,
        can_lead_from_rear=0,
        payload_by_class=[0, 0, 24],
        comfort_by_class=[0, 0, 24],
        liverytype=['LMR-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
