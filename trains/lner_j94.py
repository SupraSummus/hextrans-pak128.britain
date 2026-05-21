"""lner-j94."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-J94',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1943,
    intro_month=3,
    retire_year=1947,
    retire_month=10,
    speed=80,
    length=6,
    weight=48,
    axles=3,
    power=208,
    tractive_effort=106,
    way_wear_factor=75600,
    payload=0,
    cost=3168000,
    runningcost=195,
    fixed_cost=26640,
    increase_maintenance_after_years=10,
    years_before_maintenance_max_reached=10,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lner-j94-br.blend',
    upstream_dat='trains/lner-j94.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
