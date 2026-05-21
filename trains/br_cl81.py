"""br-cl81."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/British_Rail_Class_81
SPEC = Vehicle(
    name='BR-Class81',
    waytype='track',
    copyright='Kieron/JamesPetts/Rollmaterial',
    freight='None',
    engine_type='electric',
    intro_year=1959,
    intro_month=11,
    retire_year=1964,
    retire_month=2,
    speed=160,
    length=10,
    weight=80.9,
    axles=4,
    power=2390,
    gear=80,
    tractive_effort=222,
    rolling_resistance=13,
    payload=0,
    cost=8785000,
    runningcost=479,
    fixed_cost=16101,
    increase_maintenance_after_years=20,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='spompeytransportvideo-class-85.wav',
    constraint_prev=['none'],
    liverytype=['BR-Revised', 'BR-Blue', 'IC-Executive', 'RfD-Two-tone-grey'],
    way_constraint_permissive=[2],
    blend='trains/Locomotives/br-cl81-br-blue.blend',
    upstream_dat='trains/br-cl81.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
