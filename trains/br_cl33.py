"""br-cl33."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class33',
    waytype='track',
    copyright='Junna/Cake',
    freight='None',
    engine_type='diesel',
    intro_year=1960,
    intro_month=2,
    retire_year=1975,
    retire_month=10,
    speed=140,
    length=9,
    weight=73,
    axles=4,
    power=1156,
    gear=50,
    tractive_effort=200,
    rolling_resistance=13,
    payload=0,
    cost=7056000,
    runningcost=579,
    fixed_cost=14900,
    increase_maintenance_after_years=11,
    bidirectional=1,
    can_lead_from_rear=1,
    smoke='Diesel',
    sound='androo4519-class-33.wav',
    constraint_prev=['BR-Class33', 'BR-Class73', 'none'],
    liverytype=['BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/br-cl33-b.blend',
    upstream_dat='trains/br-cl33.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
