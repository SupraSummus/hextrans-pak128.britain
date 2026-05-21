"""gnr-n2-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/N/n2.php
SPEC = Vehicle(
    name='gnr-n2',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1920,
    intro_month=4,
    retire_year=1929,
    retire_month=11,
    speed=107,
    length=5,
    weight=71.4,
    axle_load=19,
    power=291,
    tractive_effort=89,
    payload=0,
    cost=6757525,
    runningcost=92,
    fixed_cost=37514,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['GNR-Standard', 'LNER-Standard', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gnr-n2.blend',
    upstream_dat='trains/gnr-n2-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
