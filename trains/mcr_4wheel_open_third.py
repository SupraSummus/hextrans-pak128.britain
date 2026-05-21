"""mcr-4wheel-open-third."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Lacy & Dow p. 4
SPEC = Vehicle(
    name='mcr-4wheel-open-third',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='Passagiere',
    intro_year=1844,
    intro_month=4,
    retire_year=1856,
    retire_month=6,
    speed=130,
    length=3,
    weight=3.4,
    axles=2,
    brake_force=0,
    rolling_resistance=19,
    payload=40,
    min_loading_time=17,
    max_loading_time=47,
    overcrowded_capacity=20,
    cost=125000,
    runningcost=0,
    fixed_cost=260,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    payload_by_class=[0, 40],
    comfort_by_class=[0, 17],
    liverytype=['MR-Early', 'London-&-Birmingham-standard', 'LNWR-Early', 'GNR-early', 'LSWR-early', 'Stockton-Darlington-lake', 'ECR-standard', 'MCR-standard'],
    blend='trains/Carriages/mcr-4wheel-open-second-b&djr.blend',
    upstream_dat='trains/mcr-4wheel-open-third.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
