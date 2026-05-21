"""br-cl67."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class67',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='diesel',
    intro_year=2000,
    intro_month=2,
    speed=200,
    length=11,
    weight=90,
    axles=4,
    power=2200,
    gear=50,
    tractive_effort=144,
    brake_force=68,
    rolling_resistance=13,
    payload=0,
    cost=5670000,
    runningcost=440,
    fixed_cost=12953,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='video47-class-67.wav',
    constraint_prev=['BR-Class66', 'BR-Class67', 'BR-Class70', 'none'],
    blend='trains/Locomotives/br-cl67-ews.blend',
    upstream_dat='trains/br-cl67.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
