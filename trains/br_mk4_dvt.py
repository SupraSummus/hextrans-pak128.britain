"""br-mk4-dvt."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Mk4-DVT',
    waytype='track',
    copyright='Kieron/Rollmaterial',
    freight='Post',
    intro_year=1989,
    intro_month=11,
    retire_year=2003,
    retire_month=6,
    speed=225,
    length=11,
    weight=43,
    axles=4,
    brake_force=32,
    rolling_resistance=13,
    payload=300,
    min_loading_time=25,
    max_loading_time=160,
    cost=1030000,
    runningcost=0,
    fixed_cost=2146,
    bidirectional=0,
    can_lead_from_rear=1,
    constraint_prev=['any'],
    liverytype=['IC-Swallow', 'GNER', 'National-Express', 'East-Coast', 'VTEC', 'LNER-225'],
    blend='trains/Carriages/br-mk4-dvt-gner.blend',
    upstream_dat='trains/br-mk4-dvt.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
