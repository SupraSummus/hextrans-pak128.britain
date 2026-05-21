"""br-mk1-guv-b."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Mk1-GUV',
    waytype='track',
    copyright='Kieron',
    freight='Post',
    intro_year=1956,
    intro_month=2,
    retire_year=1960,
    retire_month=12,
    speed=150,
    length=10,
    weight=30,
    axles=4,
    payload=600,
    min_loading_time=30,
    max_loading_time=300,
    cost=581000,
    runningcost=0,
    fixed_cost=692,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    liverytype=['BR-Revised', 'RM-Early', 'RM-Revised', 'RES'],
    blend='trains/Carriages/br-mk1-guv.blend',
    upstream_dat='trains/br-mk1-guv-b.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
