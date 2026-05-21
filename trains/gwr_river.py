"""gwr-river."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_River_Class
# https://c1.staticflickr.com/3/2581/4127943633_854e27d962_b.jpg
SPEC = Vehicle(
    name='gwr-river',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1895,
    intro_month=2,
    retire_year=1902,
    retire_month=1,
    speed=131,
    length=4,
    weight=43.2,
    axle_load=16,
    power=252,
    tractive_effort=50,
    payload=0,
    cost=10240440,
    runningcost=152,
    fixed_cost=32675,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['GWR-dean-tender'],
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined'],
    blend='trains/Locomotives/gwr-river-ww1-austerity.blend',
    upstream_dat='trains/gwr-river.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
