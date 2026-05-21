"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMR-4Wheel-Open-Coach',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='Passagiere',
    intro_year=1834,
    intro_month=7,
    retire_year=1839,
    retire_month=4,
    speed=100,
    length=3,
    weight=1,
    axles=2,
    brake_force=0,
    rolling_resistance=19,
    payload=30,
    min_loading_time=17,
    max_loading_time=47,
    overcrowded_capacity=15,
    cost=67000,
    runningcost=0,
    fixed_cost=140,
    upgrade_price=15000,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    payload_by_class=[0, 0, 30],
    comfort_by_class=[0, 0, 18],
    liverytype=['LMR-Standard', 'MR-Early', 'LNWR-Early', 'GNR-early', 'LSWR-early', 'B&DJR-standard', 'MCR-standard', 'Stockton-Darlington-early', 'Stockton-Darlington-lake', 'London-&-Birmingham-standard', 'ECR-standard'],
    upgrade=['lmr-4wheel-open-second'],
    blend='trains/Carriages/4wheel-open-coach.blend',
    upstream_dat='trains/lmr-4wheel-open-coach.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
