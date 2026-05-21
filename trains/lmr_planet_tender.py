"""lmr-planet-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMR-Planet-Tender',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1830,
    intro_month=6,
    retire_year=1848,
    retire_month=8,
    speed=59,
    length=2,
    weight=1,
    brake_force=1,
    rolling_resistance=19,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=25,
    constraint_prev=['LMR-Lion', 'LMR-Planet', 'LMR-Planet-Goods', 'stevenson-goods', 'vulcan'],
    blend='trains/Locomotives/planet.blend',
    upstream_dat='trains/lmr-planet-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
