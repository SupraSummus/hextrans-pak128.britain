"""gwr-3232."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_3232_Class
# http://www.brassmasters.co.uk/images/GWR%20Finney/3245%20front%207mm.jpg
# http://www.gwr.org.uk/galperkins1.html
SPEC = Vehicle(
    name='gwr-3232',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1892,
    intro_month=4,
    retire_year=1899,
    retire_month=5,
    speed=138,
    length=4,
    weight=41.8,
    axle_load=15,
    power=228,
    tractive_effort=54,
    payload=0,
    cost=10032561,
    runningcost=148,
    fixed_cost=35271,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['GWR-dean-tender'],
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined'],
    blend='trains/Locomotives/gwr-3232-ww1-austerity.blend',
    upstream_dat='trains/gwr-3232.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
