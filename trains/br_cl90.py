"""br-cl90."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class90',
    waytype='track',
    copyright='Kieron/Rollmaterial',
    freight='None',
    engine_type='electric',
    intro_year=1987,
    intro_month=2,
    retire_year=1998,
    retire_month=10,
    speed=177,
    length=11,
    weight=85,
    axles=4,
    power=3730,
    gear=80,
    tractive_effort=258,
    brake_force=65,
    rolling_resistance=13,
    payload=0,
    cost=6552000,
    runningcost=373,
    fixed_cost=11460,
    increase_maintenance_after_years=23,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='treacher-rail-class-90.wav',
    constraint_prev=['BR-Class86', 'BR-Class87', 'BR-Class89', 'BR-Class90', 'BR-Class91', 'none'],
    liverytype=['IC-Swallow', 'GNER', 'National-Express', 'Virgin-original', 'NXEA', 'One', 'Abellio-Greater-Anglia'],
    way_constraint_permissive=[2],
    blend='trains/Locomotives/br-cl90-abellio.blend',
    upstream_dat='trains/br-cl90.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
