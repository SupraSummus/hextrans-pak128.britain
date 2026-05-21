"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lbscr-a1.blend'
_UPSTREAM_DAT = 'trains/lbscr-a1.dat'

SPECS = [
Vehicle(
    name='LBSCR-A1',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1872,
    intro_month=2,
    retire_year=1880,
    retire_month=11,
    speed=85,
    length=4,
    weight=27,
    axles=3,
    power=126,
    tractive_effort=34,
    payload=0,
    cost=4032000,
    runningcost=145,
    fixed_cost=27360,
    increase_maintenance_after_years=58,
    years_before_maintenance_max_reached=26,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    upgrade=['LBSCR-A1X'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
Vehicle(
    name='LBSCR-A1X',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1911,
    intro_month=1,
    retire_year=1923,
    retire_month=1,
    speed=85,
    length=5,
    weight=29,
    axles=3,
    power=134,
    tractive_effort=48,
    payload=0,
    cost=2016000,
    runningcost=52,
    fixed_cost=17680,
    upgrade_price=500000,
    years_before_maintenance_max_reached=26,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Stroudley', 'LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
