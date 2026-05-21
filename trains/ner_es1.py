"""ner-es1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='NER-ClassES1',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='electric',
    intro_year=1905,
    intro_month=6,
    retire_year=1919,
    retire_month=2,
    speed=75,
    length=6,
    weight=56,
    axles=4,
    power=480,
    gear=80,
    tractive_effort=111,
    payload=0,
    cost=1584000,
    runningcost=288,
    fixed_cost=11650,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='antman09ful1-class-71.wav',
    constraint_prev=['none'],
    liverytype=['NER-standard', 'LNER-Standard', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    way_constraint_permissive=[1],
    blend='trains/Locomotives/ner-es1-austerity.blend',
    upstream_dat='trains/ner-es1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
