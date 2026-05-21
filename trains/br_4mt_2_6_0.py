"""br-4mt-2-6-0."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-4MT-2-6-0',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1952,
    intro_month=12,
    retire_year=1957,
    retire_month=11,
    speed=115,
    length=6,
    weight=61,
    axle_load=17,
    power=331,
    tractive_effort=108,
    rolling_resistance=13,
    payload=0,
    cost=4621000,
    runningcost=284,
    fixed_cost=27851,
    increase_maintenance_after_years=8,
    years_before_maintenance_max_reached=11,
    bidirectional=0,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['BR-4MT-Tender'],
    blend='trains/Locomotives/br-4mt-2-6-0.blend',
    upstream_dat='trains/br-4mt-2-6-0.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
