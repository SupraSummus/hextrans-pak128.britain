"""br-cl56."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class56',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='diesel',
    intro_year=1976,
    intro_month=9,
    retire_year=1984,
    retire_month=3,
    speed=130,
    length=11,
    weight=126,
    axles=6,
    power=2420,
    gear=50,
    tractive_effort=275,
    rolling_resistance=13,
    payload=0,
    cost=6758000,
    runningcost=1211,
    fixed_cost=14693,
    increase_maintenance_after_years=16,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='video47-class-56.wav',
    constraint_prev=['BR-Class56', 'BR-Class58', 'none'],
    blend='trains/Locomotives/br-cl56-blue.blend',
    upstream_dat='trains/br-cl56.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
