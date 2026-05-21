"""sdr-locomotion-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SDR-Locomotion-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1825,
    intro_month=9,
    retire_year=1830,
    retire_month=8,
    speed=24,
    length=3,
    weight=2.25,
    brake_force=1,
    rolling_resistance=19,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=25,
    constraint_prev=['SDR-Locomotion'],
    blend='trains/Locomotives/sdr-locomotion.blend',
    upstream_dat='trains/sdr-locomotion-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
