"""gwr-2021-rebuilt."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Pannier tank version
# http://www.gwr.org.uk/nopanniers.html
# https://en.wikipedia.org/wiki/GWR_2021_Class
SPEC = Vehicle(
    name='gwr-2021-rebuilt',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1910,
    intro_month=4,
    retire_year=1931,
    retire_month=3,
    speed=85,
    length=4,
    weight=41.3,
    axle_load=14,
    power=203,
    tractive_effort=72,
    payload=0,
    cost=262500,
    runningcost=130,
    fixed_cost=21200,
    upgrade_price=58335,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-2021-rebuilt-ww1-austerity.blend',
    upstream_dat='trains/gwr-2021-rebuilt.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
