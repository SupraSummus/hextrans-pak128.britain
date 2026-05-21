"""gwr-barnum."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_3206_Class
SPEC = Vehicle(
    name='gwr-barnum',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1889,
    intro_month=10,
    retire_year=1898,
    retire_month=7,
    speed=126,
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
    blend='trains/Locomotives/gwr-barnum-ww1-austerity.blend',
    upstream_dat='trains/gwr-barnum.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
