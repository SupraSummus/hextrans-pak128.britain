"""gwr-2800-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gwr-2800-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1909,
    intro_month=10,
    retire_year=1938,
    retire_month=7,
    speed=90,
    length=6,
    weight=76.7,
    axle_load=17,
    power=442,
    tractive_effort=157,
    payload=0,
    cost=6415200,
    runningcost=155,
    fixed_cost=45399,
    upgrade_price=801900,
    smoke='Steam',
    sound='keithpeter-gwr-hall.wav',
    constraint_next=['GWR-2800-Tender'],
    liverytype=['GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-2800.blend',
    upstream_dat='trains/gwr-2800-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
