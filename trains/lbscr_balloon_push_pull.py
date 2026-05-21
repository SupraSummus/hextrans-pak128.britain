"""lbscr-balloon-push-pull."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-balloon-push-pull',
    waytype='track',
    copyright='James/jamespetts',
    freight='Passagiere',
    intro_year=1907,
    intro_month=1,
    retire_year=1920,
    retire_month=1,
    speed=160,
    length=9,
    weight=27,
    axles=4,
    payload=70,
    min_loading_time=17,
    max_loading_time=50,
    overcrowded_capacity=35,
    cost=800000,
    runningcost=0,
    fixed_cost=952,
    bidirectional=1,
    can_lead_from_rear=1,
    constraint_prev=['LBSCR-A1X'],
    constraint_next=['none'],
    payload_by_class=[0, 70],
    comfort_by_class=[0, 77],
    liverytype=['LBSCR-Marsh', 'LBSCR-Late', 'SR-Olive-Green', 'SR-Malachite-Green', 'BR-Early'],
    blend='trains/Carriages/lbscr-balloon-push-pull-malachite.blend',
    upstream_dat='trains/lbscr-balloon-push-pull.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
