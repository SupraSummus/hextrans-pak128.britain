"""br-cl58."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class58',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='diesel',
    intro_year=1982,
    intro_month=12,
    retire_year=1989,
    retire_month=7,
    speed=130,
    length=11,
    weight=130,
    axles=6,
    power=2460,
    gear=50,
    tractive_effort=267,
    rolling_resistance=13,
    payload=0,
    cost=7606000,
    runningcost=738,
    fixed_cost=13961,
    increase_maintenance_after_years=12,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='video47-class-56.wav',
    constraint_prev=['BR-Class56', 'BR-Class58', 'none'],
    blend='trains/Locomotives/br-cl58-grey.blend',
    upstream_dat='trains/br-cl58.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
