"""gwr-3150."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# These were later superheated: see http://orion.math.iastate.edu/jdhsmith/term/slgbgw.htm
SPEC = Vehicle(
    name='gwr-3150',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1906,
    intro_month=4,
    retire_year=1913,
    retire_month=3,
    speed=105,
    length=7,
    weight=82.9,
    axle_load=18,
    power=293,
    tractive_effort=114,
    payload=0,
    cost=5059584,
    runningcost=122,
    fixed_cost=43550,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    upgrade=['GWR-Prairie-Tank-Modified', 'gwr-3150-superheated'],
    blend='trains/Locomotives/gwr-3150-churchward.blend',
    upstream_dat='trains/gwr-3150.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
