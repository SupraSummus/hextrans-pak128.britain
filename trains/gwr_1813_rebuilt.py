"""gwr-1813-rebuilt."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Pannier tank version
# http://www.gwr.org.uk/nopanniers.html
# https://en.wikipedia.org/wiki/GWR_1813_Class
SPEC = Vehicle(
    name='gwr-1813-rebuilt',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1903,
    intro_month=4,
    retire_year=1930,
    retire_month=3,
    speed=87,
    length=5,
    weight=48.1,
    axle_load=17,
    power=206,
    tractive_effort=82,
    payload=0,
    cost=2212000,
    runningcost=133,
    fixed_cost=25800,
    upgrade_price=491556,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-1813-rebuilt-churchward.blend',
    upstream_dat='trains/gwr-1813-rebuilt.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
