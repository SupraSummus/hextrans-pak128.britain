"""ner-ef1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='NER-ClassEF1',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='electric',
    intro_year=1914,
    intro_month=12,
    retire_year=1940,
    retire_month=7,
    speed=85,
    length=7,
    weight=74,
    axles=4,
    power=820,
    gear=80,
    tractive_effort=146,
    payload=0,
    cost=3300000,
    runningcost=493,
    fixed_cost=13438,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='antman09ful1-class-71.wav',
    constraint_prev=['none'],
    liverytype=['NER-standard', 'LNER-Standard', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    way_constraint_permissive=[1],
    blend='trains/Locomotives/ner-ef1-austerity.blend',
    upstream_dat='trains/ner-ef1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
