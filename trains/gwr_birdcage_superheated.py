"""gwr-birdcage-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_3600_Class
# http://www.greatwestern.org.uk/m_in_242.htm
SPEC = Vehicle(
    name='gwr-birdcage-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1912,
    intro_month=10,
    retire_year=1927,
    retire_month=11,
    speed=98,
    length=6,
    weight=60.4,
    axle_load=17,
    power=306,
    tractive_effort=85,
    payload=0,
    cost=4147200,
    runningcost=99,
    fixed_cost=43350,
    upgrade_price=2166912,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-birdcage.blend',
    upstream_dat='trains/gwr-birdcage-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
