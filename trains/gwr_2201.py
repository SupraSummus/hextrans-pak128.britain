"""gwr-2201."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_2201_Class
SPEC = Vehicle(
    name='gwr-2201',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1881,
    intro_month=6,
    retire_year=1890,
    retire_month=2,
    speed=128,
    length=4,
    weight=39.8,
    axle_load=15,
    power=203,
    tractive_effort=44,
    brake_force=20,
    payload=0,
    cost=9933229,
    runningcost=122,
    fixed_cost=32348,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined'],
    blend='trains/Locomotives/gwr-2201-ww1-austerity.blend',
    upstream_dat='trains/gwr-2201.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
