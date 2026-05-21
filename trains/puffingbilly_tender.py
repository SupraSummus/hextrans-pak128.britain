"""puffingbilly-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='PuffingBilly-Tender',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1813,
    intro_month=10,
    retire_year=1815,
    retire_month=8,
    speed=10,
    length=3,
    weight=1,
    axles=2,
    brake_force=1,
    rolling_resistance=19,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=42,
    constraint_prev=['PuffingBilly'],
    blend='trains/Locomotives/puffingbilly.blend',
    upstream_dat='trains/puffingbilly-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
