"""lbscr-i3."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-I3',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1908,
    intro_month=3,
    retire_year=1921,
    retire_month=7,
    speed=130,
    length=7,
    weight=75,
    axle_load=18,
    power=291,
    tractive_effort=98,
    payload=0,
    cost=6041100,
    runningcost=120,
    fixed_cost=29034,
    increase_maintenance_after_years=24,
    years_before_maintenance_max_reached=28,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-I3-austerity.blend',
    upstream_dat='trains/lbscr-i3.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
