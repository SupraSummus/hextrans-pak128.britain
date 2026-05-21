"""lmr-patentee."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LMR-Patentee',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1833,
    intro_month=6,
    retire_year=1838,
    retire_month=12,
    speed=80,
    length=3,
    weight=10.5,
    axle_load=4,
    power=37,
    tractive_effort=5,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=28453,
    payload=0,
    cost=7257600,
    runningcost=95,
    fixed_cost=26080,
    increase_maintenance_after_years=25,
    years_before_maintenance_max_reached=70,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LMR-Patentee-Tender'],
    blend='trains/Locomotives/patentee.blend',
    upstream_dat='trains/lmr-patentee.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
