"""gnr-241-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.gnrsociety.com/locomotive-class/sturrock-0-4-2-suburban-tanks/
SPEC = Vehicle(
    name='gnr-241-class',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1865,
    intro_month=1,
    retire_year=1872,
    retire_month=12,
    speed=87,
    length=5,
    weight=40.2,
    axle_load=13,
    power=134,
    tractive_effort=39,
    rolling_resistance=17,
    way_wear_factor=57037,
    payload=0,
    cost=6213500,
    runningcost=110,
    fixed_cost=24000,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['GNR-early', 'GNR-Standard'],
    blend='trains/Locomotives/gnr-241-class-dark.blend',
    upstream_dat='trains/gnr-241-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
