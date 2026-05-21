"""gwr-aberdare-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_2600_Class
SPEC = Vehicle(
    name='gwr-aberdare-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1908,
    intro_month=12,
    retire_year=1928,
    retire_month=7,
    speed=85,
    length=5,
    weight=57,
    axle_load=17,
    power=327,
    tractive_effort=115,
    payload=0,
    cost=4621172,
    runningcost=98,
    fixed_cost=42750,
    upgrade_price=2310586,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-churchward-tender'],
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early'],
    upgrade=['gwr-aberdare-superheated'],
    blend='trains/Locomotives/gwr-aberdare.blend',
    upstream_dat='trains/gwr-aberdare-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
