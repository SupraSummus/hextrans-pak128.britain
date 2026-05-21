"""kitson-standard-3."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Gladwin pp. 109-202 of vol. 3 and pp. 64-5 of vol. 1 for data.
SPEC = Vehicle(
    name='kitson-standard-3',
    waytype='tram_track',
    copyright='jamespetts',
    engine_type='steam',
    intro_year=1886,
    intro_month=5,
    retire_year=1908,
    retire_month=4,
    speed=16,
    length=3,
    weight=11,
    axles=2,
    power=6,
    tractive_effort=18,
    cost=295000,
    runningcost=5,
    fixed_cost=16246,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='laurie-barclay-0-4-0.wav',
    constraint_prev=['none'],
    blend='trams/kitson-standard-3.blend',
    upstream_dat='trams/kitson-standard-3.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
