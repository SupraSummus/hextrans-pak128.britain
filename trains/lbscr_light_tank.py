"""lbscr-light-tank."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# "Kemp Town" tank
SPEC = Vehicle(
    name='LBSCR-light-tank',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1869,
    intro_month=1,
    retire_year=1871,
    retire_month=8,
    speed=76,
    length=4,
    weight=25,
    axles=3,
    power=93,
    tractive_effort=25,
    payload=0,
    cost=3970000,
    runningcost=112,
    fixed_cost=19308,
    increase_maintenance_after_years=58,
    years_before_maintenance_max_reached=26,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Craven', 'LBSCR-Stroudley', 'LBSCR-Marsh'],
    blend='trains/Locomotives/lbscr-light-tank-craven.blend',
    upstream_dat='trains/lbscr-light-tank.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
