"""sr-1-co-co-1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SR-1-Co-Co-1',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='diesel',
    intro_year=1950,
    intro_month=2,
    retire_year=1958,
    retire_month=9,
    speed=140,
    length=9,
    weight=135,
    axles=8,
    power=1300,
    gear=50,
    tractive_effort=214,
    payload=0,
    cost=11500000,
    runningcost=1303,
    fixed_cost=21979,
    increase_maintenance_after_years=17,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='x24tohayes-epb.wav',
    constraint_prev=['SR-1-Co-Co-1', 'none'],
    liverytype=['BR-Early', 'BR-Revised'],
    blend='trains/Locomotives/sr-1co-co1-g.blend',
    upstream_dat='trains/sr-1-co-co-1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
