"""lbscr-L."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-L',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1914,
    intro_month=4,
    retire_year=1922,
    retire_month=5,
    speed=130,
    length=8,
    weight=100,
    axle_load=19,
    power=430,
    tractive_effort=108,
    payload=0,
    cost=7795200,
    runningcost=162,
    fixed_cost=30496,
    increase_maintenance_after_years=15,
    years_before_maintenance_max_reached=21,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    liverytype=['LBSCR-Marsh', 'SR-Olive-Green'],
    blend='trains/Locomotives/lbscr-l-olive.blend',
    upstream_dat='trains/lbscr-L.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
