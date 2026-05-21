"""br-cl66."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class66',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='diesel',
    intro_year=1998,
    intro_month=9,
    retire_year=2014,
    retire_month=8,
    speed=120,
    length=12,
    weight=126,
    axles=6,
    power=2385,
    gear=50,
    tractive_effort=409,
    brake_force=95,
    rolling_resistance=13,
    payload=0,
    cost=5280000,
    runningcost=716,
    fixed_cost=12750,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='treacher-rail-class-66.wav',
    constraint_prev=['BR-Class66', 'BR-Class67', 'BR-Class70', 'none'],
    blend='trains/Locomotives/br-cl66-ews.blend',
    upstream_dat='trains/br-cl66.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
