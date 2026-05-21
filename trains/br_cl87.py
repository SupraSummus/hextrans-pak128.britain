"""br-cl87."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class87',
    waytype='track',
    copyright='Kieron/Rollmaterial',
    freight='None',
    engine_type='electric',
    intro_year=1973,
    intro_month=6,
    retire_year=1987,
    retire_month=2,
    speed=177,
    length=10,
    weight=83,
    axles=4,
    power=3730,
    gear=80,
    tractive_effort=258,
    brake_force=65,
    rolling_resistance=13,
    payload=0,
    cost=8295000,
    runningcost=561,
    fixed_cost=15760,
    increase_maintenance_after_years=20,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='treacher-rail-class-87.wav',
    constraint_prev=['BR-Class86', 'BR-Class87', 'BR-Class89', 'BR-Class90', 'BR-Class91', 'none'],
    liverytype=['BR-Blue', 'IC-Executive', 'IC-Swallow', 'Virgin-original'],
    way_constraint_permissive=[2],
    blend='trains/Locomotives/br-cl87-ic-swallow.blend',
    upstream_dat='trains/br-cl87.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
