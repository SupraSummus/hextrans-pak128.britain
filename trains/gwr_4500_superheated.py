"""gwr-4500-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_4500_Class
SPEC = Vehicle(
    name='gwr-4500-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1912,
    intro_month=7,
    retire_year=1927,
    retire_month=9,
    speed=97,
    length=6,
    weight=57.9,
    axle_load=15,
    power=257,
    tractive_effort=94,
    payload=0,
    cost=4053528,
    runningcost=92,
    fixed_cost=39120,
    upgrade_price=730000,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    blend='trains/Locomotives/gwr-4500.blend',
    upstream_dat='trains/gwr-4500-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
