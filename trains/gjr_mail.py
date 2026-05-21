"""gjr-mail."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# These are the matching mail stowage versions of the very first
# TPO. No illustrations are available, but they are described
# (very generally) at Lacy & Dow, pp. 43-6
SPEC = Vehicle(
    name='gjr-mail',
    waytype='track',
    copyright='James/jamespetts',
    freight='Post',
    intro_year=1840,
    intro_month=5,
    retire_year=1850,
    retire_month=9,
    speed=125,
    length=3,
    weight=3.8,
    axles=2,
    brake_force=0,
    rolling_resistance=19,
    payload=240,
    min_loading_time=35,
    max_loading_time=120,
    cost=160000,
    runningcost=0,
    fixed_cost=67,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    liverytype=['LMR-Standard'],
    blend='trains/Carriages/gjr-bed-carriage.blend',
    upstream_dat='trains/gjr-mail.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
