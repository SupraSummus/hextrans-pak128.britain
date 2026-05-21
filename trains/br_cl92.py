"""br-cl92."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class92',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='electric',
    intro_year=1994,
    intro_month=6,
    speed=140,
    length=12,
    weight=126,
    axles=6,
    power=5040,
    gear=80,
    tractive_effort=360,
    brake_force=95,
    rolling_resistance=13,
    payload=0,
    cost=8800000,
    runningcost=505,
    fixed_cost=14583,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='video47-class-92.wav',
    constraint_prev=['BR-Class92', 'none'],
    blend='trains/Locomotives/br-cl92-rf.blend',
    upstream_dat='trains/br-cl92.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
