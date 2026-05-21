"""clyde-cargo-steamer."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='ClydeCargoSteamerHull',
    waytype='water',
    copyright='James',
    engine_type='steam',
    intro_year=1869,
    intro_month=11,
    retire_year=1912,
    retire_month=8,
    speed=20,
    length=10,
    weight=3500,
    power=4550,
    min_loading_time=3600,
    max_loading_time=7200,
    cost=178000000,
    runningcost=939,
    fixed_cost=154167,
    smoke='Steam',
    sound='ship-horn_b.wav',
    range=150,
    constraint_prev=['none'],
    constraint_next=['ClydeCargoSteamerAddMail', 'ClydeCargoSteamerAddLivestock', 'ClydeCargoSteamerAddPiece', 'ClydeCargoSteamerAddCool', 'ClydeCargoSteamerAddBulk', 'ClydeCargoSteamerAddLong'],
    blend='boats/clyde-cargo-steamer.blend',
    upstream_dat='boats/clyde-cargo-steamer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
