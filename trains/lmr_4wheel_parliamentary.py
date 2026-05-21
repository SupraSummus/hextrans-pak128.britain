"""lmr-4wheel-parliamentary."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Midland Railway Carriages (Vol. 1)
# by Lacy & Dow, p. 22
SPEC = Vehicle(
    name='LMR-4Wheel-Parliamentary',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='Passagiere',
    intro_year=1845,
    intro_month=11,
    retire_year=1851,
    retire_month=6,
    speed=130,
    length=3,
    weight=4.5,
    axles=2,
    brake_force=0,
    rolling_resistance=19,
    payload=30,
    min_loading_time=17,
    max_loading_time=47,
    overcrowded_capacity=15,
    cost=110000,
    runningcost=0,
    fixed_cost=92,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    payload_by_class=[0, 30],
    comfort_by_class=[0, 30],
    liverytype=['MR-Early', 'London-&-Birmingham-standard', 'LNWR-Early', 'GNR-early', 'LSWR-early', 'Stockton-Darlington-lake', 'ECR-standard'],
    blend='trains/Carriages/4wheel-parliamentary.blend',
    upstream_dat='trains/lmr-4wheel-parliamentary.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
