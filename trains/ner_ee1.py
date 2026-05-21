"""ner-ee1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='NER-ClassEE1',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='electric',
    intro_year=1922,
    intro_month=5,
    retire_year=1941,
    retire_month=1,
    speed=105,
    length=9,
    weight=111.8,
    axle_load=18,
    power=1342,
    gear=80,
    tractive_effort=125,
    payload=0,
    cost=6570000,
    runningcost=538,
    fixed_cost=14563,
    increase_maintenance_after_years=25,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='antman09ful1-class-71.wav',
    constraint_prev=['none'],
    liverytype=['NER-standard', 'LNER-Standard', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    way_constraint_permissive=[1],
    blend='trains/Locomotives/ner-ee1-austerity.blend',
    upstream_dat='trains/ner-ee1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
