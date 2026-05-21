"""gnr-n1-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/N/n1.php
SPEC = Vehicle(
    name='gnr-n1',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1907,
    intro_month=6,
    retire_year=1920,
    retire_month=11,
    speed=105,
    length=5,
    weight=66.9,
    axle_load=18,
    power=237,
    tractive_effort=72,
    payload=0,
    cost=5426100,
    runningcost=92,
    fixed_cost=33914,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['GNR-Standard', 'LNER-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gnr-n1.blend',
    upstream_dat='trains/gnr-n1-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
