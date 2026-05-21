"""sdr-1001-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SDR-1001-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1852,
    intro_month=9,
    retire_year=1875,
    retire_month=7,
    speed=48,
    length=3,
    weight=16,
    axles=3,
    brake_force=5,
    rolling_resistance=19,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    constraint_prev=['SDR-1001'],
    blend='trains/Locomotives/sdr-1001-tender.blend',
    upstream_dat='trains/sdr-1001-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
