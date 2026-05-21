"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='PSChevalier',
    waytype='water',
    copyright='jamespetts',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1866,
    intro_month=4,
    retire_year=1886,
    retire_month=5,
    speed=25,
    length=12,
    weight=400,
    power=600,
    payload=400,
    min_loading_time=2400,
    max_loading_time=2700,
    catering_level=4,
    cost=58406400,
    runningcost=65,
    fixed_cost=224336,
    smoke='Steam',
    sound='ship-horn_b.wav',
    range=65,
    constraint_prev=['none'],
    constraint_next=['PSChevalierMail'],
    payload_by_class=[0, 400, 0, 200],
    comfort_by_class=[0, 67, 0, 100],
    blend='boats/ps-chevalier.blend',
    upstream_dat='boats/ps-chevalier.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
