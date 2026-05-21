"""br-cl83."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/British_Rail_Class_83
SPEC = Vehicle(
    name='BR-Class83',
    waytype='track',
    copyright='Kieron/JamesPetts/Rollmaterial',
    freight='None',
    engine_type='electric',
    intro_year=1960,
    intro_month=7,
    retire_year=1964,
    retire_month=2,
    speed=160,
    length=9,
    weight=77.6,
    axles=4,
    power=2240,
    gear=80,
    tractive_effort=169,
    rolling_resistance=13,
    payload=0,
    cost=8795000,
    runningcost=460,
    fixed_cost=16000,
    increase_maintenance_after_years=20,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='treacher-rail-class-86.wav',
    constraint_prev=['none'],
    liverytype=['BR-Revised', 'BR-Blue', 'IC-Executive'],
    way_constraint_permissive=[2],
    blend='trains/Locomotives/br-cl83-br.blend',
    upstream_dat='trains/br-cl83.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
