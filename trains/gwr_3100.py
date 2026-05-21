"""gwr-3100."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# These were later superheated: see http://orion.math.iastate.edu/jdhsmith/term/slgbgw.htm
SPEC = Vehicle(
    name='GWR-Prairie-Tank',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1903,
    intro_month=8,
    retire_year=1913,
    retire_month=3,
    speed=105,
    length=7,
    weight=76.7,
    axle_load=18,
    power=285,
    tractive_effort=105,
    payload=0,
    cost=4147200,
    runningcost=111,
    fixed_cost=43456,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    upgrade=['gwr-5100'],
    blend='trains/Locomotives/gwr-3100-modified-black.blend',
    upstream_dat='trains/gwr-3100.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
