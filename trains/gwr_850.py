"""gwr-850."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Saddle tank version
# http://www.gwr.org.uk/nopanniers.html
# https://en.wikipedia.org/wiki/GWR_850_Class
SPEC = Vehicle(
    name='gwr-850',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1874,
    intro_month=2,
    retire_year=1910,
    retire_month=10,
    speed=76,
    length=4,
    weight=38.7,
    axle_load=13,
    power=141,
    tractive_effort=55,
    payload=0,
    cost=2500000,
    runningcost=122,
    fixed_cost=20300,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined'],
    upgrade=['gwr-850-rebuilt'],
    blend='trains/Locomotives/gwr-850-rebuilt-ww1-austerity.blend',
    upstream_dat='trains/gwr-850.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
