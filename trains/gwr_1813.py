"""gwr-1813."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Side tank version
# http://www.gwr.org.uk/nopanniers.html
# https://en.wikipedia.org/wiki/GWR_1813_Class
SPEC = Vehicle(
    name='gwr-1813',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1882,
    intro_month=10,
    retire_year=1903,
    retire_month=5,
    speed=85,
    length=5,
    weight=48.1,
    axle_load=17,
    power=203,
    tractive_effort=65,
    payload=0,
    cost=2200000,
    runningcost=136,
    fixed_cost=25850,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined'],
    upgrade=['gwr-1813-rebuilt'],
    blend='trains/Locomotives/gwr-1813-churchward-ww1-austerity.blend',
    upstream_dat='trains/gwr-1813.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
