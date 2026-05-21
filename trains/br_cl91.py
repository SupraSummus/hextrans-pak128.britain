"""br-cl91."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class91',
    waytype='track',
    copyright='Kieron/Rollmaterial',
    freight='None',
    engine_type='electric',
    intro_year=1988,
    intro_month=1,
    retire_year=2003,
    retire_month=6,
    speed=225,
    length=11,
    weight=84,
    axles=4,
    power=4700,
    gear=80,
    brake_force=65,
    rolling_resistance=13,
    payload=0,
    cost=14800000,
    runningcost=471,
    fixed_cost=18333,
    bidirectional=0,
    can_lead_from_rear=1,
    sound='stuart-class-91.wav',
    constraint_prev=['BR-Class86', 'BR-Class87', 'BR-Class89', 'BR-Class90', 'BR-Class91', 'none'],
    liverytype=['IC-Swallow', 'GNER', 'National-Express', 'East-Coast', 'VTEC', 'LNER-225'],
    way_constraint_permissive=[2],
    blend='trains/Locomotives/br-cl91-gner.blend',
    upstream_dat='trains/br-cl91.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
