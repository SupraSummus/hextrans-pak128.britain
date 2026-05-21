"""mr-4wheel-1848-second."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Lacy & Dow p. 22 and 16. Although based on a Midland
# vehicle, these can be given liveries for all contemporary
# railway companies, as the types did not vary greatly.
_BLEND = 'trains/Carriages/mr-4wheel-1848-varnished.blend'
_UPSTREAM_DAT = 'trains/mr-4wheel-1848-second.dat'

SPECS = [
    Vehicle(
        name='mr-4wheel-1848-second',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1847,
        intro_month=5,
        retire_year=1851,
        retire_month=7,
        speed=125,
        length=3,
        weight=6.2,
        axles=2,
        brake_force=0,
        rolling_resistance=19,
        payload=24,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=12,
        cost=165000,
        runningcost=0,
        fixed_cost=138,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['any'],
        constraint_next=['any'],
        payload_by_class=[0, 0, 24],
        comfort_by_class=[0, 0, 38],
        liverytype=['MR-Early', 'LNWR-Early', 'GNR-early', 'LSWR-early', 'Stockton-Darlington-lake', 'ECR-standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='mr-4wheel-1848-second-brake-front',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1847,
        intro_month=5,
        retire_year=1851,
        retire_month=7,
        speed=125,
        length=3,
        weight=6.2,
        axles=2,
        brake_force=2,
        rolling_resistance=19,
        payload=24,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=12,
        cost=166000,
        runningcost=0,
        fixed_cost=4938,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['any'],
        constraint_next=['any'],
        payload_by_class=[0, 0, 24],
        comfort_by_class=[0, 0, 38],
        liverytype=['MR-Early', 'LNWR-Early', 'GNR-early', 'LSWR-early', 'Stockton-Darlington-lake', 'ECR-standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='mr-4wheel-1848-second-brake-rear',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1847,
        intro_month=5,
        retire_year=1851,
        retire_month=7,
        speed=125,
        length=3,
        weight=6.2,
        axles=2,
        brake_force=2,
        rolling_resistance=19,
        payload=24,
        min_loading_time=17,
        max_loading_time=47,
        overcrowded_capacity=12,
        cost=166000,
        runningcost=0,
        fixed_cost=4938,
        bidirectional=1,
        can_lead_from_rear=0,
        payload_by_class=[0, 0, 24],
        comfort_by_class=[0, 0, 38],
        liverytype=['MR-Early', 'LNWR-Early', 'GNR-early', 'LSWR-early', 'Stockton-Darlington-lake', 'ECR-standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
