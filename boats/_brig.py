"""brig."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BrigHull',
    waytype='water',
    copyright='Druid/James',
    engine_type='sail',
    intro_year=1700,
    intro_month=1,
    retire_year=1880,
    retire_month=6,
    speed=15,
    length=6,
    weight=80,
    power=440,
    cost=7500000,
    runningcost=1,
    fixed_cost=85208,
    constraint_prev=['none'],
    constraint_next=['BrigAddPax', 'BrigAddBulk', 'BrigAddMail', 'BrigAddPiece', 'BrigAddCool', 'BrigAddLong', 'BrigAddLivestock', 'BrigAddPax-first-class'],
    blend='boats/brig.blend',
    upstream_dat='boats/brig.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
