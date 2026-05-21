"""mr-4wheel-composite."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# This is based on the SDR composite preserved at the NRM.
SPEC = Vehicle(
    name='mr-4wheel-composite',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='Passagiere',
    intro_year=1845,
    intro_month=11,
    retire_year=1850,
    retire_month=6,
    speed=130,
    length=3,
    weight=4.8,
    axles=2,
    brake_force=0,
    rolling_resistance=19,
    payload=16,
    min_loading_time=17,
    max_loading_time=47,
    overcrowded_capacity=8,
    cost=123000,
    runningcost=0,
    fixed_cost=103,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    payload_by_class=[0, 0, 16, 6],
    comfort_by_class=[0, 0, 39, 58],
    liverytype=['MR-Early', 'London-&-Birmingham-standard', 'LNWR-Early', 'GNR-early', 'LSWR-early', 'Stockton-Darlington-lake', 'ECR-standard'],
    blend='trains/Carriages/mr-4wheel-1848-lnwr.blend',
    upstream_dat='trains/mr-4wheel-composite.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
