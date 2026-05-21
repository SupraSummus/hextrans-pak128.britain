"""gwr-buffalo-rebuilt."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Pannier tank version
# http://www.gwr.org.uk/nopanniers.html
# https://en.wikipedia.org/wiki/GWR_1076_Class
SPEC = Vehicle(
    name='gwr-buffalo-rebuilt',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1911,
    intro_month=10,
    retire_year=1929,
    retire_month=9,
    speed=85,
    length=5,
    weight=47.9,
    axle_load=16,
    power=189,
    tractive_effort=80,
    payload=0,
    cost=2100000,
    runningcost=122,
    fixed_cost=24800,
    upgrade_price=466666,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-buffalo-rebuilt-ww1-austerity.blend',
    upstream_dat='trains/gwr-buffalo-rebuilt.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
