"""gwr-481."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_481_Class
SPEC = Vehicle(
    name='gwr-481',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1868,
    intro_month=1,
    retire_year=1875,
    retire_month=5,
    speed=110,
    length=4,
    weight=37.9,
    axle_load=14,
    power=176,
    tractive_effort=40,
    brake_force=0,
    payload=0,
    cost=10727889,
    runningcost=215,
    fixed_cost=29950,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown'],
    blend='trains/Locomotives/gwr-481-churchward.blend',
    upstream_dat='trains/gwr-481.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
