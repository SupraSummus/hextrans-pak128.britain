"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='manning-wardle-2-6-2t',
    waytype='narrowgauge_track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1898,
    intro_month=5,
    retire_year=1925,
    retire_month=10,
    speed=72,
    length=4,
    weight=27.7,
    axle_load=6,
    power=55,
    tractive_effort=30,
    rolling_resistance=19,
    payload=0,
    cost=3140561,
    runningcost=47,
    fixed_cost=16875,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='the-mart-ban-wllr-tank.wav',
    liverytype=['L&BR-Standard', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early', 'FR-Green-Cream', 'FR-Cherry-Red'],
    upgrade=['manning-wardle-2-6-2t-superheated'],
    blend='narrowgauge/manning-wardle-2-6-2t.blend',
    upstream_dat='narrowgauge/manning-wardle-2-6-2t.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
