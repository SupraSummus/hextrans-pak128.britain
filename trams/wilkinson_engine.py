"""wilkinson-engine."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Gladwin (vol. 1) p. 65 for illustrations
# and pp. 109-202 of vol. 3 and pp. 64-5 of vol. 1 for data.
SPEC = Vehicle(
    name='wilkinson-engine',
    waytype='tram_track',
    copyright='jamespetts',
    engine_type='steam',
    intro_year=1881,
    intro_month=1,
    retire_year=1887,
    retire_month=8,
    speed=16,
    length=3,
    weight=5.5,
    axle_load=3,
    power=3,
    tractive_effort=9,
    cost=230000,
    runningcost=3,
    fixed_cost=16192,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='laurie-barclay-0-4-0.wav',
    constraint_prev=['none'],
    blend='trams/wilkinson-engine.blend',
    upstream_dat='trams/wilkinson-engine.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
