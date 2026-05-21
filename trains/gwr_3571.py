"""gwr-3571."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_3571_class
SPEC = Vehicle(
    name='gwr-3571',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1895,
    intro_month=3,
    retire_year=1922,
    retire_month=11,
    speed=90,
    length=5,
    weight=41.7,
    axles=3,
    power=199,
    tractive_effort=75,
    payload=0,
    cost=7360000,
    runningcost=201,
    fixed_cost=32200,
    upgrade_price=2030000,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-3571-ww1-austerity.blend',
    upstream_dat='trains/gwr-3571.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
