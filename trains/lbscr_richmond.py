"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-Richmond',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1878,
    intro_month=6,
    retire_year=1883,
    retire_month=9,
    speed=127,
    length=4,
    weight=37.6,
    axle_load=14,
    power=214,
    tractive_effort=56,
    payload=0,
    cost=8700000,
    runningcost=204,
    fixed_cost=31250,
    increase_maintenance_after_years=40,
    years_before_maintenance_max_reached=35,
    bidirectional=0,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LBSCR-Belgravia-tender'],
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh'],
    blend='trains/Locomotives/lbscr-richmond.blend',
    upstream_dat='trains/lbscr-richmond.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
