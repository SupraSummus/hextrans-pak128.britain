"""gnr-120-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.gnrsociety.com/locomotive-class/120-class/
SPEC = Vehicle(
    name='gnr-120-class',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1872,
    intro_month=10,
    retire_year=1882,
    retire_month=1,
    speed=96,
    length=5,
    weight=41.4,
    axle_load=15,
    power=153,
    tractive_effort=51,
    way_wear_factor=65812,
    payload=0,
    cost=7456200,
    runningcost=126,
    fixed_cost=25000,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['GNR-early', 'GNR-Standard'],
    blend='trains/Locomotives/gnr-120-class-dark.blend',
    upstream_dat='trains/gnr-120-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
