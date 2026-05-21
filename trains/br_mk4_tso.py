"""br-mk4-tso."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Mk4-TSO',
    waytype='track',
    copyright='Kieron/Rollmaterial',
    freight='Passagiere',
    intro_year=1989,
    intro_month=11,
    retire_year=2003,
    retire_month=6,
    speed=225,
    length=13,
    weight=40,
    axles=4,
    brake_force=32,
    rolling_resistance=13,
    payload=74,
    min_loading_time=25,
    max_loading_time=160,
    overcrowded_capacity=21,
    cost=592000,
    runningcost=0,
    fixed_cost=1233,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_next=['BR-Mk4-TSO', 'BR-Mk4-DVT', 'BR-Mk4-RSB', 'BR-Mk4-FO'],
    payload_by_class=[0, 74, 0, 0],
    comfort_by_class=[0, 149, 0, 172],
    liverytype=['IC-Swallow', 'GNER', 'National-Express', 'East-Coast', 'VTEC', 'LNER-225'],
    blend='trains/Carriages/br-mk4-dvt-ec.blend',
    upstream_dat='trains/br-mk4-tso.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
