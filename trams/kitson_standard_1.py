"""kitson-standard-1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Gladwin (vol. 1) p. 65 for illustrations
# and pp. 109-202 of vol. 3 and pp. 64-5 of vol. 1 for data.
SPEC = Vehicle(
    name='kitson-standard-1',
    waytype='tram_track',
    copyright='jamespetts',
    engine_type='steam',
    intro_year=1879,
    intro_month=6,
    retire_year=1883,
    retire_month=1,
    speed=16,
    length=3,
    weight=7.0,
    axle_load=4,
    power=3,
    tractive_effort=12,
    cost=200000,
    runningcost=3,
    fixed_cost=16167,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='laurie-barclay-0-4-0.wav',
    constraint_prev=['none'],
    blend='trams/kitson-standard-1.blend',
    upstream_dat='trams/kitson-standard-1.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
