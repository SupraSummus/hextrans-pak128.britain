"""jennylind-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='JennyLind-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1846,
    intro_month=1,
    retire_year=1858,
    retire_month=4,
    speed=105,
    length=3,
    weight=15,
    axles=3,
    rolling_resistance=19,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    constraint_prev=['JennyLind', 'lbscr-gray-single'],
    liverytype=['LBSCR-Early', 'LBSCR-Craven'],
    blend='trains/Locomotives/jennylind-tender-craven.blend',
    upstream_dat='trains/jennylind-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
