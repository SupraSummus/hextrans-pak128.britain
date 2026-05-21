"""br-cl29."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class29',
    waytype='track',
    copyright='Junna/Cake',
    freight='None',
    engine_type='diesel',
    intro_year=1963,
    intro_month=1,
    retire_year=1967,
    retire_month=9,
    speed=130,
    length=9,
    weight=74,
    axles=4,
    power=1010,
    gear=50,
    tractive_effort=200,
    rolling_resistance=13,
    payload=0,
    runningcost=505,
    fixed_cost=10000,
    upgrade_price=1125000,
    increase_maintenance_after_years=25,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    constraint_prev=['BR-Class16', 'BR-Class21', 'BR-Class28', 'BR-Class29', 'BR-Class30', 'none'],
    liverytype=['BR-Early', 'BR-Blue'],
    blend='trains/Locomotives/br-cl29-green.blend',
    upstream_dat='trains/br-cl29.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
