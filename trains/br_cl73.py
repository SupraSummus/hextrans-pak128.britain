"""br-cl73."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class73',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='electric',
    intro_year=1962,
    intro_month=12,
    retire_year=1974,
    retire_month=9,
    speed=145,
    length=10,
    weight=77,
    axles=4,
    power=1059,
    gear=80,
    tractive_effort=178,
    rolling_resistance=13,
    payload=0,
    cost=5040000,
    runningcost=159,
    fixed_cost=13500,
    increase_maintenance_after_years=22,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='antman09ful1-class-71.wav',
    constraint_prev=['BR-Class33', 'BR-Class73', 'none'],
    liverytype=['BR-Revised', 'BR-Blue', 'BR-Large-Logo', 'IC-Executive', 'IC-Swallow'],
    way_constraint_permissive=[0],
    blend='trains/Locomotives/br-cl73-ic.blend',
    upstream_dat='trains/br-cl73.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
