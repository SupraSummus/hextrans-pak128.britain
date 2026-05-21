"""gwr-2021."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Saddle tank version
# http://www.gwr.org.uk/nopanniers.html
# https://en.wikipedia.org/wiki/GWR_2021_Class
SPEC = Vehicle(
    name='gwr-2021',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1897,
    intro_month=6,
    retire_year=1910,
    retire_month=10,
    speed=82,
    length=4,
    weight=41.3,
    axle_load=14,
    power=197,
    tractive_effort=72,
    payload=0,
    cost=2620000,
    runningcost=130,
    fixed_cost=21300,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity'],
    upgrade=['gwr-2021-rebuilt'],
    blend='trains/Locomotives/gwr-2021-rebuilt-ww1-austerity.blend',
    upstream_dat='trains/gwr-2021.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
