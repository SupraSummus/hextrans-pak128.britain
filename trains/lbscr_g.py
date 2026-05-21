"""lbscr-g."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-G',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1874,
    intro_month=1,
    retire_year=1882,
    retire_month=6,
    speed=125,
    length=4,
    weight=36.2,
    axle_load=14,
    power=206,
    tractive_effort=48,
    payload=0,
    cost=9975000,
    runningcost=242,
    fixed_cost=32313,
    increase_maintenance_after_years=40,
    years_before_maintenance_max_reached=35,
    bidirectional=0,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LBSCR-Belgravia-tender'],
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh'],
    blend='trains/Locomotives/lbscr-g-umber.blend',
    upstream_dat='trains/lbscr-g.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
