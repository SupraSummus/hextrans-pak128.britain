"""gwr-stella."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_3201_Class
SPEC = Vehicle(
    name='gwr-stella',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1884,
    intro_month=3,
    retire_year=1892,
    retire_month=9,
    speed=87,
    length=4,
    weight=43.2,
    axle_load=16,
    power=252,
    tractive_effort=61,
    payload=0,
    cost=10240440,
    runningcost=152,
    fixed_cost=32675,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['GWR-dean-tender'],
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined'],
    blend='trains/Locomotives/gwr-stella-ww1-austerity.blend',
    upstream_dat='trains/gwr-stella.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
