"""kitson-standard-2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Gladwin (vol. 1) pp. 66-67 for illustrations
# and pp. 109-202 of vol. 3 and pp. 64-5 of vol. 1 for data.
SPEC = Vehicle(
    name='kitson-standard-2',
    waytype='tram_track',
    copyright='jamespetts',
    engine_type='steam',
    intro_year=1882,
    intro_month=11,
    retire_year=1891,
    retire_month=3,
    speed=16,
    length=3,
    weight=9.5,
    axles=2,
    power=4,
    tractive_effort=16,
    cost=210000,
    runningcost=4,
    fixed_cost=16175,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='laurie-barclay-0-4-0.wav',
    constraint_prev=['none'],
    blend='trams/kitson-standard-2.blend',
    upstream_dat='trams/kitson-standard-2.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
