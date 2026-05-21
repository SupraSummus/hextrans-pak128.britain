"""br-cl47."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class47',
    waytype='track',
    copyright='Kieron/Rollmaterial',
    freight='None',
    engine_type='diesel',
    intro_year=1962,
    intro_month=9,
    retire_year=1972,
    retire_month=1,
    speed=153,
    length=11,
    weight=127.0,
    axles=6,
    power=1922,
    gear=50,
    tractive_effort=255,
    rolling_resistance=13,
    payload=0,
    cost=6912000,
    runningcost=962,
    fixed_cost=14800,
    increase_maintenance_after_years=24,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel-heavy',
    sound='video47-class-47.wav',
    constraint_prev=['BR-Class47', 'none'],
    liverytype=['BR-Revised', 'BR-Blue', 'BR-Large-Logo', 'Scotrail-original', 'IC-Executive', 'IC-Swallow', 'NSE-Revised', 'NSE-Standard', 'Railfreight-grey', 'RM-Revised', 'TF-Two-tone-grey', 'RfD-Two-tone-grey', 'Virgin-original', 'Anglia-original', 'One'],
    upgrade=['BR-Class57'],
    blend='trains/Locomotives/br-cl47-rf-two-tone-plain.blend',
    upstream_dat='trains/br-cl47.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
