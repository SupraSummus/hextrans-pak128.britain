"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='RMSColumba',
    waytype='water',
    copyright='jamespetts',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1878,
    intro_month=6,
    retire_year=1901,
    retire_month=9,
    speed=39,
    length=12,
    weight=500,
    power=650,
    payload=1500,
    min_loading_time=2400,
    max_loading_time=2700,
    catering_level=5,
    cost=318000000,
    runningcost=107,
    fixed_cost=732500,
    smoke='Steam',
    sound='ship-horn_a.wav',
    range=130,
    constraint_prev=['none'],
    constraint_next=['RMSColumbaMail'],
    payload_by_class=[0, 0, 1500, 0, 500],
    comfort_by_class=[0, 0, 122, 0, 179],
    blend='boats/rms-columba.blend',
    upstream_dat='boats/rms-columba.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
