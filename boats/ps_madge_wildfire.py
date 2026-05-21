"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='PSMadgeWildfire',
    waytype='water',
    copyright='jamespetts',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1886,
    intro_month=1,
    retire_year=1899,
    retire_month=3,
    speed=30,
    length=12,
    weight=450,
    power=600,
    payload=800,
    min_loading_time=1200,
    max_loading_time=1400,
    catering_level=4,
    cost=90000000,
    runningcost=66,
    fixed_cost=237500,
    smoke='Steam',
    sound='ship-horn_b.wav',
    range=120,
    constraint_prev=['none'],
    constraint_next=['PSMadgeWildfireMail'],
    payload_by_class=[0, 800, 0, 183],
    comfort_by_class=[0, 82, 0, 109],
    blend='boats/ps-madge-wildfire.blend',
    upstream_dat='boats/ps-madge-wildfire.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
