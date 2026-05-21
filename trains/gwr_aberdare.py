"""gwr-aberdare."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_2600_Class
SPEC = Vehicle(
    name='gwr-aberdare',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1900,
    intro_month=8,
    retire_year=1907,
    retire_month=9,
    speed=85,
    length=5,
    weight=57,
    axle_load=17,
    power=284,
    tractive_effort=107,
    payload=0,
    cost=4201065,
    runningcost=102,
    fixed_cost=42700,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['GWR-dean-tender'],
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early'],
    upgrade=['gwr-aberdare-superheated'],
    blend='trains/Locomotives/gwr-aberdare-ww1-austerity.blend',
    upstream_dat='trains/gwr-aberdare.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
