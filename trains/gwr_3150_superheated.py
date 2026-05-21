"""gwr-3150-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gwr-3150-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1912,
    intro_month=12,
    retire_year=1930,
    retire_month=1,
    speed=105,
    length=7,
    weight=80.0,
    axle_load=18,
    power=326,
    tractive_effort=114,
    payload=0,
    cost=5312569,
    runningcost=110,
    fixed_cost=43552,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    liverytype=['GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    upgrade=['GWR-Prairie-Tank-Modified'],
    blend='trains/Locomotives/gwr-3150.blend',
    upstream_dat='trains/gwr-3150-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
