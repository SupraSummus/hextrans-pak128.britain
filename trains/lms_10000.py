"""lms-10000."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMS-10000',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='diesel',
    intro_year=1947,
    intro_month=10,
    retire_year=1960,
    retire_month=6,
    speed=150,
    length=11,
    weight=129.7,
    axles=6,
    power=1200,
    gear=50,
    tractive_effort=184,
    payload=0,
    cost=11491200,
    runningcost=1203,
    fixed_cost=21970,
    increase_maintenance_after_years=15,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='lwalker-class-40.wav',
    constraint_prev=['LMS-10000', 'none'],
    liverytype=['LMS-Standard', 'BR-Early', 'BR-Revised', 'BR-Blue'],
    blend='trains/Locomotives/lms-10000-br-black.blend',
    upstream_dat='trains/lms-10000.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
