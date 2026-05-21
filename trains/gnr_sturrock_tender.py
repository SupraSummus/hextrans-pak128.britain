"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gnr-sturrock-tender',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1860,
    intro_month=4,
    retire_year=1885,
    retire_month=7,
    speed=130,
    length=4,
    weight=20,
    axles=3,
    brake_force=3,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    constraint_prev=['gnr-a-class', 'gnr-h-class', 'GNR-Stirling7Foot', 'gnr-sturrock-single'],
    liverytype=['GNR-early', 'GNR-Standard', 'LNER-Standard'],
    blend='trains/Locomotives/gnr-sturrock-tender.blend',
    upstream_dat='trains/gnr-sturrock-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
