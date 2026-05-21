"""gwr-850-rebuilt."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Pannier tank version
# http://www.gwr.org.uk/nopanniers.html
# https://en.wikipedia.org/wiki/GWR_850_Class
SPEC = Vehicle(
    name='gwr-850-rebuilt',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1910,
    intro_month=1,
    retire_year=1933,
    retire_month=7,
    speed=76,
    length=4,
    weight=38.7,
    axle_load=14,
    power=152,
    tractive_effort=71,
    payload=0,
    cost=3200000,
    runningcost=122,
    fixed_cost=20200,
    upgrade_price=55555,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-850-rebuilt-ww1-austerity.blend',
    upstream_dat='trains/gwr-850-rebuilt.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
