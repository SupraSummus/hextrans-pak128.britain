"""gwr-4500."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_4500_Class
SPEC = Vehicle(
    name='gwr-4500',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1906,
    intro_month=11,
    retire_year=1912,
    retire_month=12,
    speed=97,
    length=6,
    weight=57.9,
    axle_load=15,
    power=237,
    tractive_effort=88,
    payload=0,
    cost=3753267,
    runningcost=99,
    fixed_cost=39000,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    upgrade=['gwr-4500-superheated'],
    blend='trains/Locomotives/gwr-4500-churchward.blend',
    upstream_dat='trains/gwr-4500.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
