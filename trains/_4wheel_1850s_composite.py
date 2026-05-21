"""4wheel-1850s-composite."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='4-wheel-1850s-composite',
    waytype='track',
    copyright='James/jamespetts',
    freight='Passagiere',
    intro_year=1850,
    intro_month=9,
    retire_year=1859,
    retire_month=10,
    speed=135,
    length=3,
    weight=8.1,
    axles=2,
    brake_force=0,
    rolling_resistance=19,
    payload=16,
    min_loading_time=17,
    max_loading_time=47,
    overcrowded_capacity=8,
    cost=161000,
    runningcost=0,
    fixed_cost=134,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    payload_by_class=[0, 0, 16, 6],
    comfort_by_class=[0, 38, 41, 69],
    liverytype=['LNWR-Early', 'MR-Early', 'MR-Standard', 'GNR-early', 'LSWR-Indian-red', 'GWR-early', 'GWR-two-tone'],
    blend='trains/Carriages/4wheel-1850.blend',
    upstream_dat='trains/4wheel-1850s-composite.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
