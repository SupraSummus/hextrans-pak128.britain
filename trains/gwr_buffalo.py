"""gwr-buffalo."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Saddle tank version
# http://www.gwr.org.uk/nopanniers.html
# https://en.wikipedia.org/wiki/GWR_1076_Class
SPEC = Vehicle(
    name='gwr-buffalo',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1870,
    intro_month=10,
    retire_year=1882,
    retire_month=12,
    speed=85,
    length=5,
    weight=47.8,
    axle_load=16,
    power=176,
    tractive_effort=62,
    payload=0,
    cost=2100000,
    runningcost=160,
    fixed_cost=24900,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown'],
    upgrade=['gwr-buffalo-rebuilt'],
    blend='trains/Locomotives/gwr-buffalo-rebuilt-ww1-austerity.blend',
    upstream_dat='trains/gwr-buffalo.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
