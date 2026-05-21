"""gwr-birdcage."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_3600_Class
# http://www.greatwestern.org.uk/m_in_242.htm
SPEC = Vehicle(
    name='gwr-birdcage',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1900,
    intro_month=2,
    retire_year=1909,
    retire_month=9,
    speed=98,
    length=6,
    weight=60.3,
    axle_load=17,
    power=274,
    tractive_effort=81,
    payload=0,
    cost=3939840,
    runningcost=108,
    fixed_cost=43021,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
    upgrade=['gwr-birdcage-superheated'],
    blend='trains/Locomotives/gwr-birdcage-ww1-austerity.blend',
    upstream_dat='trains/gwr-birdcage.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
