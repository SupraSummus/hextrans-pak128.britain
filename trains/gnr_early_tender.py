"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gnr-early-tender',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1847,
    intro_month=8,
    retire_year=1867,
    retire_month=9,
    speed=110,
    length=3,
    weight=15,
    axles=3,
    brake_force=2,
    rolling_resistance=19,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    constraint_prev=['gnr-sturrock-coupled', 'gnr-hawthorn-single', 'gnr-wilson-single'],
    liverytype=['GNR-early', 'GNR-Standard'],
    blend='trains/Locomotives/gnr-early-tender.blend',
    upstream_dat='trains/gnr-early-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
