"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='manning-wardle-2-6-2t-superheated',
    waytype='narrowgauge_track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1925,
    intro_month=7,
    retire_year=1956,
    retire_month=4,
    speed=72,
    length=4,
    weight=27.7,
    axle_load=6,
    power=72,
    tractive_effort=32,
    rolling_resistance=18,
    payload=0,
    cost=3611645,
    runningcost=36,
    fixed_cost=16875,
    upgrade_price=656663,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='the-mart-ban-wllr-tank.wav',
    liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early', 'FR-Green-Cream', 'FR-Cherry-Red'],
    blend='narrowgauge/manning-wardle-2-6-2t.blend',
    upstream_dat='narrowgauge/manning-wardle-2-6-2t-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
