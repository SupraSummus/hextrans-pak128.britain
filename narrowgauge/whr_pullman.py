"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='WHR-pullman',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Passagiere',
    intro_year=1998,
    intro_month=5,
    speed=80,
    length=6,
    weight=10,
    axles=4,
    rolling_resistance=17,
    payload=20,
    min_loading_time=20,
    max_loading_time=65,
    cost=1021000,
    runningcost=0,
    fixed_cost=1575,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    payload_by_class=[0, 0, 0, 20],
    comfort_by_class=[0, 67, 67, 155],
    liverytype=['Pullman-Cream-Umber'],
    blend='narrowgauge/whr-pullman.blend',
    upstream_dat='narrowgauge/whr-pullman.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
