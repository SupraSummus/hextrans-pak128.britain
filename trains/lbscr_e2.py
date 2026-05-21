"""lbscr-e2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-E2',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1913,
    intro_month=5,
    retire_year=1920,
    retire_month=3,
    speed=92,
    length=6,
    weight=53.6,
    axles=3,
    power=237,
    tractive_effort=95,
    payload=0,
    cost=3900000,
    runningcost=93,
    fixed_cost=27250,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-e2-austerity.blend',
    upstream_dat='trains/lbscr-e2.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
