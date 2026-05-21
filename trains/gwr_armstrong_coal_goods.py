"""gwr-armstrong-coal-goods."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_927_Class
SPEC = Vehicle(
    name='gwr-armstrong-coal-goods',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1866,
    intro_month=12,
    retire_year=1883,
    retire_month=7,
    speed=75,
    length=4,
    weight=30.2,
    axle_load=11,
    power=192,
    tractive_effort=65,
    brake_force=0,
    payload=0,
    cost=14001450,
    runningcost=211,
    fixed_cost=28050,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined'],
    blend='trains/Locomotives/gwr-armstrong-goods-churchward.blend',
    upstream_dat='trains/gwr-armstrong-coal-goods.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
